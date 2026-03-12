from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ContactForm
from .utils import send_contact_email

CONSENT_COOKIE_NAME = getattr(settings, "COOKIE_CONSENT_NAME", "cookie_consent")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            if not request.COOKIES.get(CONSENT_COOKIE_NAME):
                form.add_error(None, "Prosím potvrďte nastavenie cookies pred odoslaním formulára.")
                return render(request, "contact_form/contact_form.html", {"form": form})

            if not form.cleaned_data.get("consent"):
                form.add_error("consent", "Musíte súhlasiť so spracovaním osobných údajov.")
                return render(request, "contact_form/contact_form.html", {"form": form})

            subject = f"Сообщение от {form.cleaned_data['name']}"
            body = f"Email: {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}"
            send_contact_email(subject, body, reply_to=form.cleaned_data["email"])
            return redirect("contact_form:success")
    else:
        form = ContactForm()

    return render(request, "contact_form/contact_form.html", {"form": form})
