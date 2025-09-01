from django.db import models

# Create your models here.
class ClaimList(models.Model):
    patient_name = models.CharField(max_length=100)
    billed_amount = models.DecimalField(max_digits=20, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=100)
    insurer_name = models.CharField(max_length=100)
    discharge_date = models.DateField()

    def __str__(self):
        return f"ID: {self.id} - Patient Name: {self.patient_name}"
    
class ClaimDetail(models.Model):
    claim_id = models.ForeignKey(ClaimList, on_delete=models.CASCADE)
    denial_reason = models.CharField(max_length=255)
    cpt_codes = models.CharField(max_length=100)

    def __str__(self):
        return f"ID: {self.id} - Claim ID: {self.claim_id}"
    
class Employee(models.Model):
    employee_first_name = models.CharField(max_length=255)
    employee_last_name = models.CharField(max_length=255)
    employee_password = models.CharField(max_length=255, null=True, blank=True)
    employee_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} - Name: {self.employee_first_name} {self.employee_last_name} - Employee Type: {self.employee_type}"
    
class Note(models.Model):
    claim_id = models.ForeignKey(ClaimList, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} - Claim ID: {self.claim_id} - User ID: {self.claim_id}"
    
class Annotation(models.Model):
    claim_id = models.ForeignKey(ClaimList, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} - Claim ID: {self.claim_id} - User ID: {self.claim_id}"
    
class Flag(models.Model):
    claim_id = models.ForeignKey(ClaimList, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('claim_id', 'user_id')

    def __str__(self):
        return f"ID: {self.id} - Claim ID: {self.claim_id} - User ID: {self.claim_id}"