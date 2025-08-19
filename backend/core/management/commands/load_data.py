import json
import csv
from pathlib import Path
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Load .csv or .json file into database."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path for .csv or .json file.")

    def handle(self, *args, **options):
        file_path = Path(options["file_path"])

        if not file_path.exists():
            self.stdout.write(f"Error: File path does not exist.")
            return
        
        if file_path.suffix == ".csv":
            self.read_csv(file_path)
        else:
            self.stdout.write("Error: Could not find file path.")

    
    def read_csv(self, path):
        count = 0
        with open(path, mode='r') as file:
            csv_file = csv.DictReader(file, delimiter='|')
            for row in csv_file:
                self.stdout.write(f"Entry {count}: {row}")
                count+=1
    
    #def read_json(self, path):
