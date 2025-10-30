from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "first_name", "last_name", "email", "service", "status", "gdpr_consent")
    list_filter  = ("service", "status", "gdpr_consent", "created_at")
    search_fields = ("first_name", "last_name", "email", "message")
    readonly_fields = ("created_at", "updated_at", "client_ip", "user_agent", "referrer", "consent_at", "consent_version")
