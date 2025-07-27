from django.contrib import admin
from .models import Property, PropertyImage, OfficeUnit, OfficeUnitImage
from django.utils.html import format_html


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    readonly_fields = ('preview',)  # 👈 превьюшки только для просмотра
    fields = ('image', 'description', 'preview')  # порядок отображения
    verbose_name = "Фото"
    verbose_name_plural = "Фотографии"

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 4px; box-shadow: 0 0 5px #ccc;" />',
                obj.image.url
            )
        return "(нет изображения)"
    preview.short_description = "Превью"

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('name', 'type', 'location', 'created_at')
    


# properties/admin.py
from .models import OfficeUnit, OfficeUnitImage


class OfficeUnitImageInline(admin.TabularInline):
    model = OfficeUnitImage
    extra = 1
    readonly_fields = ('preview',)
    fields = ('image', 'description', 'preview')


@admin.register(OfficeUnit)
class OfficeUnitAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'floor', 'unit_number', 'area_sqm', 'price_per_month', 'status')
    list_filter = ('property', 'status', 'floor')
    search_fields = ('unit_number', 'property__name')
    ordering = ('floor', 'unit_number')
    inlines = [OfficeUnitImageInline]
