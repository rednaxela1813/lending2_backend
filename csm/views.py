from django.shortcuts import render, redirect
from .models import HeroSection, HeaderSection, FooterInfo, CompanyInfo, FrontendTheme, ServiceSection, CarouselImage, HotDealItem, HotDealSection, Icon, BottomCTASection
from properties.models import Property
from datetime import datetime
from django.utils import timezone
import pytz
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q
from django.db.models import Prefetch
import itertools

# импорт модели из contact_form
from contact_form.models import EmailSettings
from contact_form.forms import ContactForm
from contact_form.utils import send_contact_email
from django.contrib import messages



def is_working_hours():
    tz = pytz.timezone('Europe/Bratislava')
    now = datetime.now(tz)
    return now.weekday() < 5 and 9 <= now.hour < 17

def _assign_missing_icons_round_robin():
    """
    Назначает иконки только тем HotDealItem, у кого они ещё не заданы.
    Если иконок нет — просто ничего не делает.
    """
    icon_ids = list(Icon.objects.order_by('key').values_list('id', flat=True))
    if not icon_ids:
        return
    pool = itertools.cycle(icon_ids)
    to_update = []
    for obj in (HotDealItem.objects
                .filter(is_active=True, icon__isnull=True)
                .order_by('sort_order', '-updated_at')):
        obj.icon_id = next(pool)
        to_update.append(obj)
    if to_update:
        HotDealItem.objects.bulk_update(to_update, ['icon'])


def homepage(request):
    # ---- прочие секции/данные как у тебя ----
    hero_section = HeroSection.objects.first()
    header_section = HeaderSection.objects.first()
    footer_info = FooterInfo.objects.first()
    company_info = CompanyInfo.objects.first()
    theme_color = FrontendTheme.objects.filter(is_active=True).first()
    nas_sluzby = ServiceSection.objects.all()
    phone_number = company_info.phone if company_info else None
    carousel_images = CarouselImage.objects.all()

    services = {
        'office':   Property.objects.filter(type__slug='office').first(),
        'address':  Property.objects.filter(type__slug='address').first(),
        'billboard':Property.objects.filter(type__slug='billboard').first(),
    }
    total_services = sum(1 for s in services.values() if s)

    email_config = EmailSettings.objects.first()
    show_form = bool(email_config)

    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        subject = f"Správa od {form.cleaned_data['name']}"
        body = f"Email: {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}"
        if email_config and email_config.email_host_user:
            send_contact_email(subject, body, to_email=email_config.email_host_user)
            messages.success(request, "Správa bola úspešne odoslaná.")
        else:
            messages.error(request, "Email nie je nakonfigurovaný.")
        return redirect("homepage")

    # --- ВАЖНО: раздаём иконки, затем берём данные раздельно ---
    _assign_missing_icons_round_robin()

    hot_deal_section = HotDealSection.objects.filter(is_active=True).first()  # один объект с заголовками
    hot_deal_items = (HotDealItem.objects
                      .filter(is_active=True)
                      .select_related('icon')
                      .order_by('sort_order', '-updated_at'))                # много карточек

    bottom_cta_section = BottomCTASection.objects.first()  # один объект с CTA внизу

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
        'phone_number': phone_number,
        'carousel_images': carousel_images,

        # --- Раздельно! ---
        'hot_deal_section': hot_deal_section,   # один объект
        'hot_deal_items': hot_deal_items,       # queryset
        'bottom_cta_section': bottom_cta_section,  # один объект
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
