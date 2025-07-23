from django.shortcuts import render, redirect
from .models import HeroSection, HeaderSection, FooterInfo, CompanyInfo, FrontendTheme, ServiceSection
from .forms import ContactRequestForm
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.contrib import messages
from properties.models import Property
from datetime import datetime
import pytz
import requests
import logging
import re  # ✅ для улучшенного спам-фильтра

logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID


def is_working_hours():
    """Проверка: рабочее ли сейчас время (Пн-Пт, 9-17 по Братиславе)"""
    tz = pytz.timezone('Europe/Bratislava')
    now = datetime.now(tz)
    return now.weekday() < 5 and 9 <= now.hour < 17


@csrf_protect
def homepage(request):
    # Получаем данные для секций сайта
    hero_section = HeroSection.objects.first()
    header_section = HeaderSection.objects.first()
    footer_info = FooterInfo.objects.first()
    company_info = CompanyInfo.objects.first()
    theme_color = FrontendTheme.objects.filter(is_active=True).first()
    nas_sluzby = ServiceSection.objects.all()

    # Услуги (по одному объекту каждого типа)
    services = {
        'office': Property.objects.filter(type='office').first(),
        'address': Property.objects.filter(type='address').first(),
        'billboard': Property.objects.filter(type='billboard').first(),
    }
    total_services = sum(1 for s in services.values() if s)

    # Форма обратной связи
    form_failed = False
    form = ContactRequestForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            honeypot_value = form.cleaned_data.get('honeypot')
            if honeypot_value:
                logger.warning("Honeypot triggered, form submission blocked.")
                messages.error(request, "Invalid form submission.")
            else:
                name = form.cleaned_data['name']
                contact = form.cleaned_data['contact']
                message = form.cleaned_data['message']

                # ✅ Улучшенный антиспам-фильтр (ищет URL или HTML теги)
                if re.search(r'(https?://|<.*?>)', message, re.IGNORECASE):
                    logger.warning("Spam detected in contact form submission.")
                    messages.error(request, "Your message was flagged as spam.")
                else:
                    text = (
                        f"📩 *Nová žiadosť z formulára:*\n\n"
                        f"👤 *Meno:* {name}\n"
                        f"📞 *Kontakt:* {contact}\n"
                        f"💬 *Správa:*\n{message}"
                    )
                    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                    payload = {
                        "chat_id": TELEGRAM_CHAT_ID,
                        "text": text,
                        "parse_mode": "Markdown"
                    }

                    try:
                        # ✅ Добавлен таймаут
                        response = requests.post(telegram_url, json=payload, timeout=5)
                        response.raise_for_status()
                        logger.info(f"Message sent to Telegram from {name}")
                        messages.success(request, "Your message has been sent successfully.")
                        return redirect('/')  # предотвращаем повторную отправку формы
                    except requests.RequestException as e:
                        logger.error(f"Failed to send message to Telegram: {e}")
                        messages.error(request, "Failed to send your message. Please try again later.")
        else:
            logger.warning("Invalid contact form submission.")
            form_failed = True
            messages.error(request, "Formulár obsahuje chyby.")

    context = {
        'hero_section': hero_section,
        'header_section': header_section,
        'footer_info': footer_info,
        'company_info': company_info,
        'theme_color': theme_color,
        'form': form,
        'form_failed': form_failed,
        'services': services,
        'total_services': total_services,
        'nas_sluzby': nas_sluzby,
        'is_working_hours': is_working_hours(), 
    }

    return render(request, 'csm/index.html', context)
