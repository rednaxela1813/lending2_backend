from django.db import models


class EmailSettings(models.Model):
    """
    Model to store email settings for the contact form.
    """
    email_host = models.CharField(max_length=255, help_text="SMTP server address")
    email_port = models.PositiveIntegerField(help_text="SMTP server port")
    email_host_user = models.EmailField(help_text="SMTP server username")
    email_host_password = models.CharField(max_length=255, help_text="SMTP server password")
    use_tls = models.BooleanField(default=True, help_text="Use TLS for email connection")
    gdpr_compliant = models.BooleanField(default=False)
    
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email_host_user} ({'GDPR OK' if self.gdpr_compliant else 'NO GDPR'})"
