from django.conf import settings
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from apps.contact_messages.utils import anonymize_ip
from apps.site_email.services import send_contact_message_email
from .models import ContactMessage

CONSENT_COOKIE_NAME = getattr(settings, "COOKIE_CONSENT_NAME", "cookie_consent")


def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        # берём первый IP из цепочки
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        ip = xff.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return anonymize_ip(ip)


def _has_cookie_consent(request):
    return bool(request.COOKIES.get(CONSENT_COOKIE_NAME))


def submit(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    if not _has_cookie_consent(request):
        return render(request, "cookie/consent_required.html", status=403)

    first_name = request.POST.get("first_name", "").strip()
    last_name  = request.POST.get("last_name", "").strip()
    email      = request.POST.get("email", "").strip()
    service    = request.POST.get("service", "").strip()
    message    = request.POST.get("message", "").strip()
    gdpr       = request.POST.get("gdpr_consent") in ("on", "true", "1", "yes")

    if not (first_name and last_name and email and service):
        return HttpResponseBadRequest("Missing required fields.")
    if not gdpr:
        return HttpResponseBadRequest("GDPR consent is required.")

    contact_message = ContactMessage.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        service=service,
        message=message,
        gdpr_consent=True,
        consent_at=timezone.now(),
        consent_version=getattr(settings, "PRIVACY_POLICY_VERSION", "v1"),
        client_ip=_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        referrer=request.META.get("HTTP_REFERER", ""),
        source_path=request.path,
    )

    # fire-and-forget email notification; errors are logged
    send_contact_message_email(contact_message)

    # редирект на «спасибо» (или на главную с якорем)
    return HttpResponseRedirect(reverse("contact_messages:success"))

def success(request):
    # минимальный шаблон можно не делать, вернуть простой рендер или редирект назад с флагом
    return render(request, "contact_messages/success.html")
