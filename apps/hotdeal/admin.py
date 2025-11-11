# apps/hotdeal/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import HotDealItem


@admin.register(HotDealItem)
class HotDealItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "unit_display",
        "content_type",
        "is_active",
        "new_price",
        "date_expiry",
    )
    list_display_links = ("id", "title")
    list_filter = ("is_active", "content_type", "date_expiry")
    search_fields = ("title", "description", "property_name")
    readonly_fields = ("public_id",)
    ordering = ("id",)  # ← заменили

    actions = ["make_active", "make_inactive"]

    def unit_display(self, obj):
        """Ссылка на связанный юнит в админке (офис/билборд/и т.д.)."""
        label = str(getattr(obj, "content_object", None) or f"{obj.content_type}:{obj.object_id}")
        try:
            ct = obj.content_type
            url = reverse(f"admin:{ct.app_label}_{ct.model}_change", args=[obj.object_id])
            return format_html('<a href="{}">{}</a>', url, label)
        except Exception:
            return label

    unit_display.short_description = "Unit"

    @admin.action(description="Activate selected")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
