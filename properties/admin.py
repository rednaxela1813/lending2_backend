from django.contrib import admin
from .models import Property, PropertyImage
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
