from django.core.mail import EmailMessage, get_connection
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from .models import EmailSettings
import socket


def send_contact_email(subject, body, to_email):
    print("📨 Начинаем отправку письма...")

    if settings.DEBUG:
        print("🛠 DEBUG режим — используем консольный бэкенд")
        connection = get_connection(backend='django.core.mail.backends.console.EmailBackend')
        from_email = 'dev@deilmann.sk'
    else:
        config = EmailSettings.objects.first()
        if not config or not config.gdpr_compliant:
            raise ImproperlyConfigured("❌ Нет валидной конфигурации EmailSettings")

        backend_params = {
            "backend": "django.core.mail.backends.smtp.EmailBackend",
            "host": config.email_host,
            "port": config.email_port,
            "username": config.email_host_user,
            "password": config.email_host_password,
            "timeout": 10,
        }

        if getattr(config, "use_ssl", False):
            print("🔒 Используем SSL")
            backend_params["use_ssl"] = True
            backend_params["use_tls"] = False
        else:
            print("🔐 Используем TLS")
            backend_params["use_ssl"] = False
            backend_params["use_tls"] = config.use_tls

        # проверка подключения к SMTP серверу
        try:
            print(f"🌍 Проверка соединения с {config.email_host}:{config.email_port}...")
            socket.create_connection((config.email_host, config.email_port), timeout=5)
            print("✅ SMTP сервер доступен")
        except Exception as e:
            print("❌ Невозможно подключиться к SMTP серверу:", e)
            return

        connection = get_connection(**backend_params)
        from_email = config.email_host_user

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[to_email],
        connection=connection
    )

    try:
        print("📤 Письмо отправляется...")
        email.send(fail_silently=False)
        print("✅ Email успешно отправлен!")
    except Exception as e:
        print("❌ Ошибка отправки email:", e)
