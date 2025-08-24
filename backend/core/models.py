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