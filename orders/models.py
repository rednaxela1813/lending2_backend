from django.db import models
import uuid


class LegalAddressOrder(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    address_choice = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    address_choice = models.CharField(max_length=50, choices=[('nitra', 'Nitra'), ('bratislava', 'Bratislava')])
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} — {self.address_choice}"
    # Add any additional fields or methods as needed
