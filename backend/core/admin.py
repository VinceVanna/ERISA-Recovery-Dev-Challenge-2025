from django.contrib import admin
from .models import ClaimList, ClaimDetail, Employee, Note, Annotation, Flag
# Register your models here.

admin.site.register(ClaimList)
admin.site.register(ClaimDetail)
admin.site.register(Employee)
admin.site.register(Note)
admin.site.register(Annotation)
admin.site.register(Flag)