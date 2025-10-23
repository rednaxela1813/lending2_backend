from django.shortcuts import render, redirect
from .models import HeroSection, HeaderSection, FooterInfo, CompanyInfo, FrontendTheme, ServiceSection, CarouselImage, HotDealItem
from properties.models import Property
from datetime import datetime
from django.utils import timezone
import pytz
from django.urls import reverse
from django.views.generic import ListView


# импорт модели из contact_form
from contact_form.models import EmailSettings
from contact_form.forms import ContactForm
from contact_form.utils import send_contact_email
from django.contrib import messages



def is_working_hours():
    tz = pytz.timezone('Europe/Bratislava')
    now = datetime.now(tz)
    return now.weekday() < 5 and 9 <= now.hour < 17

def _build_hot_deal_context():
    today = timezone.now().date()
    hot_deal_section = HotDealItem.objects.filter(is_active=True).order_by('sort_order').first()

    if not hot_deal_section:
        return None

    offer = hot_deal_section
    # day expiry logic
    expires_in_days = (offer.date_expiry - today).days if offer.date_expiry else None
    
    return {
        "section_title": hot_deal_section.title or "Hot Deals",
        "section_subtitle": hot_deal_section.additional_description,
        "title": offer.title,
        "description": offer.description,
        "old_price": offer.old_price,
        "new_price": offer.new_price,
        "sale_circle_text": offer.badge_text,
        "sale_circle_percent": offer.badge_percent,
        "additional_description": offer.additional_description,
        "color_theme": offer.color_theme,
        "promo_list": [
            offer.promo_1,
            offer.promo_2,
            offer.promo_3,
            offer.promo_4,
        ],
        "date_expiry": offer.date_expiry,
        "expires_in_days": expires_in_days,   # ← для «Expires in N days»
        "button_text": offer.button_text or "Contact us",
        "phone_fallback": "+421 000 000 000", # если хочешь показать «Call»
    }

        
    


def homepage(request):
    hero_section = HeroSection.objects.first()
    header_section = HeaderSection.objects.first()
    footer_info = FooterInfo.objects.first()
    company_info = CompanyInfo.objects.first()
    theme_color = FrontendTheme.objects.filter(is_active=True).first()
    nas_sluzby = ServiceSection.objects.all()
    phone_number = company_info.phone if company_info else None
    # Получение изображений для карусели
    carousel_images = CarouselImage.objects.all()

    hot_deal = _build_hot_deal_context()

    services = {
        'office': Property.objects.filter(type__slug='office').first(),
        'address': Property.objects.filter(type__slug='address').first(),
        'billboard': Property.objects.filter(type__slug='billboard').first(),
    }
    total_services = sum(1 for s in services.values() if s)

    # ✨ проверка, можно ли показывать форму
    email_config = EmailSettings.objects.first()
    #show_form = email_config and email_config.gdpr_compliant
    show_form = email_config 
    
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        subject = f"Správa od {form.cleaned_data['name']}"
        body = f"Email: {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}"
        send_contact_email(subject, body, to_email=email_config.email_host_user)
        messages.success(request, "Správa bola úspešne odoslaná.")
        return redirect("homepage")  # или на отдельную success-страницу


    context = {
        'hero_section': hero_section,
        'header_section': header_section,
        'footer_info': footer_info,
        'company_info': company_info,
        'theme_color': theme_color,
        'services': services,
        'total_services': total_services,
        'nas_sluzby': nas_sluzby,
        'is_working_hours': is_working_hours(),
        'show_form': show_form,
        'form': form,
        'phone_number': phone_number,  # Можно вынести в CompanyInfo
        'carousel_images': carousel_images,  # Добавляем изображения в контекст
        'hot_deal': hot_deal,
    }

    return render(request, 'csm/index.html', context)


class ServicesListView(ListView):
    model = Property  # или как у тебя теперь называется
    template_name = 'csm/components/ServiceSection.html'
    context_object_name = 'services'

    def get_queryset(self):
        service_type = self.kwargs['service_type']
        return self.model.objects.filter(type__slug=service_type)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["hot_deal"] = _build_hot_deal_context()
        return ctx
