from django.db import models
from django.utils import timezone
import uuid
from .crypto_fields import EncryptedEmailField, EncryptedTextField
import hashlib


def _normalize_email(value: str) -> str:
    return (value or "").strip().lower()

def _email_sha256(value: str) -> str:
    return hashlib.sha256(_normalize_email(value).encode("utf-8")).hexdigest()



class ContactMessage(models.Model):
    class Service(models.TextChoices):
        OFFICE_SPACE = 'office_space', 'Office Space'
        BILLBOARD = 'billboard', 'Billboard Advertising'
        LEGAL_ADDRESS = 'legal_address', 'Legal Address'
        MULTIPLE = 'multiple', 'Multiple Services'
        
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'
        ARCHIVED = 'archived', 'Archived'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = EncryptedEmailField()
    email_hash  = models.CharField(max_length=64, db_index=True, blank=True)
    service = models.CharField(max_length=50, choices=Service.choices)
    message = EncryptedTextField(blank=True, null=True)
    
    gdpr_consent = models.BooleanField(default=False)
    consent_version = models.CharField(max_length=20, blank=True, null=True)
    consent_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    
    #audit
    client_ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    
    source_path = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["service"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["email"]),
        ]
        
    def save(self, *args, **kwargs):
        self.email_hash = _email_sha256(self.email) if self.email else ""
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}> [{self.service}]"
