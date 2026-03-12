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
from apps.hotdeal.context import build_hot_deal_items   # hot deal card builder
from apps.hotdeal.models import HotDealItem, HotDealSection  # correct import from apps.hotdeal
# contact_form model import
from contact_form.models import EmailSettings
from contact_form.forms import ContactForm
from contact_form.utils import send_contact_email


def is_working_hours():
    """Return True if current Bratislava time is within weekday business hours."""
    tz = pytz.timezone('Europe/Bratislava')
    now = datetime.now(tz)
    return now.weekday() < 5 and 9 <= now.hour < 17


def _assign_missing_icons_round_robin():
    """
    (Optional) Assign icons to HotDeals cards in a round-robin manner.
    The current HotDealItem model does not have an icon field; add it and a migration to use this.
    """
    return
    # Example if an icon field is added to HotDealItem
    icon_ids = list(Icon.objects.order_by('key').values_list('id', flat=True))
    if not icon_ids:
        return
    pool = itertools.cycle(icon_ids)
    to_update = []
    for obj in (HotDealItem.objects
                .filter(is_active=True, icon__isnull=True)
                .order_by('order', 'id')):  # legacy sort fields removed
        obj.icon_id = next(pool)
        to_update.append(obj)
    if to_update:
        HotDealItem.objects.bulk_update(to_update, ['icon'])


class HotDealsPageView(TemplateView):
    """Render the Hot Deals landing page."""
    template_name = "csm/hot_deals.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["hot_deal_items"] = build_hot_deal_items()
        # HotDealSection currently lacks is_active/order; take the first record
        ctx["hot_deal_section"] = HotDealSection.objects.order_by("id").first()
        return ctx


def homepage(request):
    """Render the homepage with hero, services, carousel, hot deals, and contact form handling."""
    hero_section = HeroSection.objects.first()
    header_section = HeaderSection.objects.first()
    footer_info = FooterInfo.objects.select_related('company').first()
    company_info = CompanyInfo.objects.first()
    theme_color = FrontendTheme.objects.filter(is_active=True).first()
    nas_sluzby = ServiceSection.objects.prefetch_related('icon_svg').all()
    phone_number = company_info.phone if company_info else None
    carousel_images = CarouselImage.objects.all()

    # Use the same slugs across the site (plural) to avoid mismatches with list views/filters
    services = {
        "office": Property.objects.filter(type__slug="offices").first(),
        "address": Property.objects.filter(type__slug="addresses").first(),
        "billboard": Property.objects.filter(type__slug="billboards").first(),
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

    # Icon assignment for HotDeals is disabled; see helper function for notes.
    _assign_missing_icons_round_robin()

    hot_deal_section = HotDealSection.objects.first()

    hot_deal_items = build_hot_deal_items()

    bottom_cta_section = BottomCTASection.objects.first()

    

    today = timezone.localdate()
    upcoming_specials = (
        company_info.special_openings.filter(date__gte=today).order_by("date")
        if company_info
        else None
    )
    next_closed = (
        upcoming_specials.filter(is_closed=True).first()
        if upcoming_specials is not None
        else None
    )

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
        'upcoming_specials': upcoming_specials,
        'next_closed_weekday': next_closed.date.weekday() if next_closed else None,

        'hot_deal_section': hot_deal_section,
        'hot_deal_items': hot_deal_items,
        'bottom_cta_section': bottom_cta_section,
    }
    return render(request, 'csm/index.html', context)


class ServicesListView(ListView):
    """List services filtered by property type slug."""
    model = Property
    template_name = 'csm/components/ServiceSection.html'
    context_object_name = 'services'

    def get_queryset(self):
        service_type = self.kwargs['service_type']
        return self.model.objects.filter(type__slug=service_type)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Include hot deals on pages where services are listed.
        ctx["hot_deal_items"] = build_hot_deal_items()
        return ctx


class ServiceDetailView(DetailView):
    """Display a specific service with related property imagery."""
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

        # Gather images from properties of the same type for background use.
        if self.object and self.object.property_type:
            props = (
                Property.objects.filter(type=self.object.property_type)
                .prefetch_related("images")
            )
            for prop in props:
                for img in prop.images.all():
                    images_pool.append(img.image.url)

        # Only use backgrounds from matching property types; fall back to none if empty.
        ctx["random_bg_image"] = random.choice(images_pool) if images_pool else None
        return ctx


class ServiceOffersListView(ListView):
    """List concrete property offers for a given service type slug."""
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
#     template_name = "csm/services_list.html"   # single template variant
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


def footer_section(request):
    """Render footer component with company info and services."""
    footer_info = FooterInfo.objects.select_related('company').first()
    company_info = CompanyInfo.objects.first()
    services = ServiceSection.objects.all()
    context = {
        'footer_info': footer_info,
        'company_info': company_info,
        'services': services,
    }
    return render(request, 'csm/components/FooterSection.html', context)
