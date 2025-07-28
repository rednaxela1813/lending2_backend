from django.core.mail import EmailMessage, get_connection
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from .models import EmailSettings


def send_contact_email(subject, body, to_email):
    if settings.DEBUG:
        # 👉 В режиме отладки отправляем письмо в консоль
        connection = get_connection(backend='django.core.mail.backends.console.EmailBackend')
        from_email = 'rednaxela1813@gmail.com'
    else:
        # 👉 В продакшене используем настройки из БД
        config = EmailSettings.objects.first()
        if not config or not config.gdpr_compliant:
            raise ImproperlyConfigured("Нет допустимой email-конфигурации")

        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=config.email_host,
            port=config.email_port,
            username=config.email_host_user,
            password=config.email_host_password,
            use_tls=config.use_tls
        )
        from_email = config.email_host_user

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[to_email],
        connection=connection
    )

    try:
        print('Письмо отправляется...')
        email.send(fail_silently=False)
        print("✅ Email отправлен (или записан в консоль)")
    except Exception as e:
        print("❌ Ошибка отправки email:", e)
