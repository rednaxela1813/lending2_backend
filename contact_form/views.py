from django.shortcuts import render, redirect
from .models import EmailSettings
from .forms import ContactForm
from .utils import send_contact_email


def contact_view(request):
    email_config = EmailSettings.objects.first()
    if not email_config or not email_config.gdpr_compliant:
        return render(request, "contact_form/phone_only.html", {
            "phone_number": "{{ COMPANY_PHONE }}"  # Можно вынести в CompanyInfo
        })

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"Сообщение от {form.cleaned_data['name']}"
            body = f"Email: {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}"
            send_contact_email(subject, body, to_email=email_config.email_host_user)
            return redirect("contact_form:success")
    else:
        form = ContactForm()

    return render(request, "contact_form/contact_form.html", {"form": form})
