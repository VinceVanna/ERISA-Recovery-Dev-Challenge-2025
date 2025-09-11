from django.contrib import admin
from .models import ClaimList, ClaimDetail, Employee, Note, Annotation, Flag


class ClaimListAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'billed_amount', 'paid_amount', 'status', 'insurer_name', 'discharge_date', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'status', 'discharge_date')
    ordering = ('-updated_at',)

class ClaimDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'claim_id', 'denial_reason', 'cpt_codes', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'claim_id')
    ordering = ('-updated_at',)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_username', 'employee_first_name', 'employee_last_name', 'employee_password', 'employee_type', 'created_at', 'updated_at')
    list_filter = ('employee_username', 'employee_first_name', 'employee_last_name', 'employee_type', 'created_at', 'updated_at')
    ordering = ('-updated_at',)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'claim_id', 'employee_id', 'content', 'created_at', 'updated_at')
    list_filter = ('claim_id', 'employee_id', 'created_at','updated_at')
    ordering = ('-updated_at',)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'claim_id', 'employee_id', 'content', 'created_at', 'updated_at')
    list_filter = ('claim_id', 'employee_id', 'created_at','updated_at')
    ordering = ('-updated_at',)

class FlagAdmin(admin.ModelAdmin):
    list_display = ('id', 'claim_id', 'employee_id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'employee_id')
    ordering = ('-updated_at',)


admin.site.register(ClaimList, ClaimListAdmin)
admin.site.register(ClaimDetail, ClaimDetailAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Flag, FlagAdmin)