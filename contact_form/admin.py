from django.contrib import admin
from .models import EmailSettings


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ('email_host_user', 'email_host', 'email_port', 'use_tls', 'use_ssl', 'gdpr_compliant', 'updated')
    readonly_fields = ('updated',)
