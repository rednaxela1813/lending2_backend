from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Property, PropertyImage, PropertyType,
    OfficeUnit, OfficeUnitImage,
    BillboardUnit, BillboardUnitImage,
    LegalAddressUnit, LegalAddressUnitImage,
)

# ───────────────────────────
# Общие inline для фото
# ───────────────────────────

class ImagePreviewInline(admin.TabularInline):
    """Базовый inline с превью"""
    extra = 1
    readonly_fields = ("preview",)
    fields = ("image", "description", "preview")

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:100px;border-radius:6px;box-shadow:0 0 5px #ccc;">',
                obj.image.url,
            )
        return "(нет изображения)"
    preview.short_description = "Превью"


# ───────────────────────────
# Property
# ───────────────────────────

class PropertyImageInline(ImagePreviewInline):
    model = PropertyImage
    verbose_name = "Фото объекта"
    verbose_name_plural = "Фотографии объекта"


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ("name", "type", "location", "created_at", "availability")
    search_fields = ("name", "location", "type__name")
    list_filter = ("type", "availability")
    ordering = ("-created_at",)
    fieldsets = [
        ("Основное", {"fields": ("name", "type", "summary", "description", "location", "map_embed_url")}),
        ("Цена и статус", {"fields": ("price", "currency", "availability", "busy_until")}),
    ]


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
   # prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)


# ───────────────────────────
# OfficeUnit
# ───────────────────────────

class OfficeUnitImageInline(ImagePreviewInline):
    model = OfficeUnitImage
    verbose_name = "Фото офиса"
    verbose_name_plural = "Фотографии офиса"


@admin.register(OfficeUnit)
class OfficeUnitAdmin(admin.ModelAdmin):
    inlines = [OfficeUnitImageInline]
    list_display = ("__str__", "property", "floor", "unit_number", "area_sqm", "price_per_month", "availability", "id")
    list_filter = ("property", "floor", "availability")
    search_fields = ("unit_number", "property__name")
    ordering = ("property", "floor", "unit_number")
    readonly_fields = ("public_id",)


# ───────────────────────────
# BillboardUnit
# ───────────────────────────

class BillboardUnitImageInline(ImagePreviewInline):
    model = BillboardUnitImage
    verbose_name = "Фото билборда"
    verbose_name_plural = "Фотографии билборда"


@admin.register(BillboardUnit)
class BillboardUnitAdmin(admin.ModelAdmin):
    inlines = [BillboardUnitImageInline]
    list_display = ("__str__", "property", "size", "price_per_month", "availability")
    list_filter = ("property", "availability")
    search_fields = ("property__name", "size")
    ordering = ("property", "id")


# ───────────────────────────
# LegalAddressUnit
# ───────────────────────────

class LegalAddressUnitImageInline(ImagePreviewInline):
    model = LegalAddressUnitImage
    verbose_name = "Фото юр. адреса"
    verbose_name_plural = "Фотографии юр. адреса"


@admin.register(LegalAddressUnit)
class LegalAddressUnitAdmin(admin.ModelAdmin):
    inlines = [LegalAddressUnitImageInline]
    list_display = ("__str__", "property", "price_per_year", "availability")
    list_filter = ("property", "availability")
    search_fields = ("property__name", "registration_number")
    ordering = ("property", "id")
