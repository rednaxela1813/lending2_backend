from django.shortcuts import render, redirect
from .models import HeroSection, HeaderSection, FooterInfo, CompanyInfo,  FrontendTheme
from django.views.generic.edit import FormView
from .forms import ContactRequestForm  # Assuming you have a ContactForm defined in forms.py
from django.views.decorators.csrf import csrf_protect
import logging
from django.conf import settings
from django.contrib import messages
import requests





logger = logging.getLogger(__name__)


TELEGRAM_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID
ALLOWED_ORIGINS = settings.ALLOWED_ORIGINS




@csrf_protect
def homepage(request):
    hero_section = HeroSection.objects.first()
    header_section = HeaderSection.objects.first()
    footer_info = FooterInfo.objects.first()
    company_info = CompanyInfo.objects.first()
    theme_color = FrontendTheme.objects.filter(is_active=True).first()
    
    form_failed = False

    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        print("POST data:", request.POST)
        print("CLEANED:", form.cleaned_data if form.is_valid() else form.errors)

        if form.is_valid():
            
            if form.cleaned_data.get('honeypot'):
                logger.warning("Honeypot triggered, form submission blocked.")
                messages.error(request, "Invalid form submission.")
            else:
                name = form.cleaned_data['name']
                contact = form.cleaned_data['contact']
                message = form.cleaned_data['message']

                if any(s in message.lower() for s in ["http://", "https://", "<script>"]):
                    logger.warning("Spam detected in contact form submission.")
                    messages.error(request, "Your message was flagged as spam.")
                else:
                    text = f"📩 *Nová žiadosť z formulára:*\n\n👤 *Meno:* {name}\n📞 *Kontakt:* {contact}\n💬 *Správa:*\n{message}"
                    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                    payload = {
                        "chat_id": TELEGRAM_CHAT_ID,
                        "text": text,
                        "parse_mode": "Markdown"
                    }

                    try:
                        response = requests.post(telegram_url, json=payload)
                        response.raise_for_status()
                        logger.info(f"Message sent to Telegram from {name}")
                        messages.success(request, "Your message has been sent successfully.")
                        return redirect('/')  # prevent form resubmission
                    except requests.RequestException as e:
                        logger.error(f"Failed to send message to Telegram: {e}")
                        messages.error(request, "Failed to send your message. Please try again later.")
        else:
            messages.error(request, "Form is invalid.")
            
        
        
        if not form.is_valid():
            messages.error(request, "Formulár obsahuje chyby.")
            form_failed = True
        else:
             form_failed = False
    else:
        form = ContactRequestForm()

    context = {
        'hero_section': hero_section,
        'header_section': header_section,
        'footer_info': footer_info,
        'company_info': company_info,
        'theme_color': theme_color,
        'form': form,
        'form_failed': form_failed,
    }

    return render(request, 'csm/index.html', context)
