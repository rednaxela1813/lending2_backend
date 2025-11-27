# csm/views.py
from django.shortcuts import render, redirect
from datetime import datetime
import random
import itertools
import pytz

from django.utils import timezone
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib import messages
from django.db.models import Q, Prefetch
from apps.company.models import CompanyInfo, FooterInfo
from .models import (
    HeroSection, HeaderSection, FrontendTheme,
    ServiceSection, CarouselImage, Icon, BottomCTASection,
)
from apps.properties.models import Property, PropertyType
from apps.hotdeal.context import build_hot_deal_items   # ← наш билдер
from apps.hotdeal.models import HotDealItem, HotDealSection  # ← правильный импорт из apps.hotdeal
# импорт модели из contact_form
from contact_form.models import EmailSettings
from contact_form.forms import ContactForm
from contact_form.utils import send_contact_email


def is_working_hours():
    tz = pytz.timezone('Europe/Bratislava')
    now = datetime.now(tz)
    return now.weekday() < 5 and 9 <= now.hour < 17


def _assign_missing_icons_round_robin():
    """
    (Опционально) Раздаём иконки для карточек HotDeals,
    НО: в текущей модели HotDealItem НЕТ поля icon.
    Если хочешь — добавь в apps/hotdeal/models.py:
        icon = models.ForeignKey(Icon, null=True, blank=True, on_delete=models.SET_NULL)
    и миграцию. Пока — просто выходим.
    """
    return
    # --- Пример, если добавишь поле icon у HotDealItem ---
    icon_ids = list(Icon.objects.order_by('key').values_list('id', flat=True))
    if not icon_ids:
        return
    pool = itertools.cycle(icon_ids)
    to_update = []
    for obj in (HotDealItem.objects
                .filter(is_active=True, icon__isnull=True)
                .order_by('order', 'id')):  # было sort_order/updated_at — их нет
        obj.icon_id = next(pool)
        to_update.append(obj)
    if to_update:
        HotDealItem.objects.bulk_update(to_update, ['icon'])


class HotDealsPageView(TemplateView):
    template_name = "csm/sections/HotDealsSection.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Горячие предложения готовим билдером → получаем список словарей под шаблон
        ctx["hot_deal_items"] = build_hot_deal_items()
        # Один объект заголовка секции (если используешь отдельную модель заголовка)
        ctx["hot_deal_section"] = HotDealSection.objects.filter(is_active=True).order_by("order", "id").first()
        return ctx


def homepage(request):
    hero_section = HeroSection.objects.first()
    header_section = HeaderSection.objects.first()
    footer_info = FooterInfo.objects.select_related('company').first()
    company_info = CompanyInfo.objects.first()
    theme_color = FrontendTheme.objects.filter(is_active=True).first()
    nas_sluzby = ServiceSection.objects.prefetch_related('icon_svg').all()
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
        return redirect("csm:homepage")

    # Если иконки для HotDeals нужны — см. комментарий в функции; сейчас noop
    _assign_missing_icons_round_robin()

    # Заголовок секции (один объект)
    hot_deal_section = HotDealSection.objects.first()

    # КАРТОЧКИ: используем билдер, чтобы структура соответствовала шаблону
    hot_deal_items = build_hot_deal_items()

    bottom_cta_section = BottomCTASection.objects.first()

    

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

        'hot_deal_section': hot_deal_section,   # один объект
        'hot_deal_items': hot_deal_items,       # уже готовые словари
        'bottom_cta_section': bottom_cta_section,
    }
    return render(request, 'csm/index.html', context)


class ServicesListView(ListView):
    model = Property
    template_name = 'csm/components/ServiceSection.html'
    context_object_name = 'services'

    def get_queryset(self):
        service_type = self.kwargs['service_type']
        return self.model.objects.filter(type__slug=service_type)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # если где-то ещё нужно hot-deals внутри этой страницы
        ctx["hot_deal_items"] = build_hot_deal_items()
        return ctx


class ServiceDetailView(DetailView):
    model = ServiceSection
    template_name = "csm/service_detail.html"
    context_object_name = "service"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("icon_svg", "property_type")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        images_pool = []

        # если есть связанный property_type, собираем изображения из Property с этим типом
        if self.object and self.object.property_type:
            props = (
                Property.objects.filter(type=self.object.property_type)
                .prefetch_related("images")
            )
            for prop in props:
                for img in prop.images.all():
                    images_pool.append(img.image.url)

        # фон только из фото соответствующего типа; если их нет — остаётся белый фон
        ctx["random_bg_image"] = random.choice(images_pool) if images_pool else None
        return ctx


class ServiceOffersListView(ListView):
    model = Property
    template_name = "csm/services_list.html"
    context_object_name = "items"
    paginate_by = 12

    def get_queryset(self):
        slug = self.kwargs.get("type")
        return (
            super()
            .get_queryset()
            .select_related("type")
            .prefetch_related("images")
            .filter(type__slug=slug)
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        slug = self.kwargs.get("type")
        ctx["active_service_type"] = slug
        ctx["service_type_obj"] = PropertyType.objects.filter(slug=slug).first()
        ctx["service_types"] = (
            ServiceSection.objects.select_related("property_type")
            .exclude(property_type__isnull=True)
            .values_list("property_type__slug", "property_type__name")
        )
        images_pool = []
        for prop in ctx["items"]:
            images = list(prop.images.all())
            prop.random_image = random.choice(images).image.url if images else None
            images_pool.extend([img.image.url for img in images])
        ctx["random_bg_image"] = random.choice(images_pool) if images_pool else None
        return ctx


# class ServicesListView2(ListView):
#     model = Property
#     template_name = "csm/services_list.html"   # <- один конкретный шаблон
#     context_object_name = "items"

#     def get_queryset(self):
#         qs = super().get_queryset().filter(is_active=True)
#         service_type = self.kwargs.get("service_type") or self.request.GET.get("service_type")
#         if service_type:
#             qs = qs.filter(type__slug=service_type)
#         return qs

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx["active_service_type"] = self.kwargs.get("service_type") or self.request.GET.get("service_type")
#         return ctx
