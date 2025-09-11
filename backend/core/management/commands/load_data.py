import json
import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = "Load .csv or .json file into database."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path for .csv or .json file.")
        parser.add_argument("--model", type=str, help="Model name (ex., ClaimList or ClaimDetail)")
        parser.add_argument("--app", type=str, default='core', help="App label/dir (default: core)")

    def handle(self, *args, **options):
        file_path = Path(options['file_path'])
        model_name = options['model']
        app_name = options['app']

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"Error: File path does not exist."))
            return
        
        ModelClass = self.get_model(app_name, model_name)

        if not ModelClass:
            self.stdout.write(self.style.ERROR(f"Model {model_name} not found or does not exist."))
        if file_path.suffix == ".csv":
            self.read_csv(file_path, ModelClass)
        elif file_path.suffix == ".json":
            self.read_json(file_path, ModelClass)
        else:
            self.stdout.write(self.style.ERROR("Error: File does not contain .csv or .json"))
    
    def get_model(self, app_name, model_name):
        try:
            return apps.get_model(app_name, model_name)
        except LookupError:
            return None

    def filtered_fields(self, row, model):
        model_fields = {field.name: field for field in model._meta.fields if field.name != 'id'}
        cleaned_data = {}

        for name, value in row.items():
            if name in model_fields:
                field = model_fields[name]
                if field.is_relation and field.many_to_one:
  
                    related_model = field.related_model
                    try:
                        cleaned_data[name] = related_model.objects.get(id=value)
                    except related_model.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f"Warning: Related {related_model.__name__} with ID {value} not found for field '{name}'"
                        ))
                        cleaned_data[name] = None
                else:
                    cleaned_data[name] = value
        return cleaned_data
    
    def read_csv(self, path, ModelClass):
        created_count = 0
        updated_count = 0
        with open(path, mode='r') as file:
            csv_file = csv.DictReader(file, delimiter='|')
            for row in csv_file:
                wanted_fields = self.filtered_fields(row, ModelClass)
                claim_info, created_claim = ModelClass.objects.update_or_create(
                    id=row['id'],
                    defaults=wanted_fields
                )
                if created_claim:
                    created_count+=1
                    self.stdout.write(self.style.SUCCESS(f"Created ID: {row['id']}"))
                else:
                    updated_count+=1
                    self.stdout.write(self.style.SUCCESS(f"Updated ID: {row['id']}"))

            self.stdout.write(self.style.SUCCESS(f"\nIDs Created: {created_count}"))
            self.stdout.write(self.style.SUCCESS(f"IDs Updated: {updated_count}"))

    
    def read_json(self, path, ModelClass):
        created_count = 0
        updated_count = 0
        with open(path, 'r') as file:
            json_file = json.load(file)

            for row in json_file:
                wanted_fields = self.filtered_fields(row, ModelClass)
                claim_info, created_claim = ModelClass.objects.update_or_create(
                    id=row['id'],
                    defaults=wanted_fields
                )

                if created_claim:
                    created_count+=1
                    self.stdout.write(self.style.SUCCESS(f"Created ID: {row['id']}"))
                else:
                    updated_count+=1
                    self.stdout.write(self.style.SUCCESS(f"Updated ID: {row['id']}"))

            self.stdout.write(self.style.SUCCESS(f"\nIDs Created: {created_count}"))
            self.stdout.write(self.style.SUCCESS(f"IDs Updated: {updated_count}"))
