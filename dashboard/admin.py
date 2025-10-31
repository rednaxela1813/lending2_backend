# apps/dashboard/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import EditableText, EditableImage


@admin.register(EditableText)
class EditableTextAdmin(admin.ModelAdmin):
    list_display = ('key', 'language', 'title', 'short_text', 'is_active', 'updated_at')
    list_filter = ('language', 'is_active')
    search_fields = ('key', 'title', 'text')
    ordering = ('key',)

    def short_text(self, obj):
        return (obj.text or '')[:80] + ('…' if obj.text and len(obj.text) > 80 else '')

@admin.register(EditableImage)
class EditableImageAdmin(admin.ModelAdmin):
    list_display = ('key', 'language', 'thumb', 'alt', 'is_active', 'updated_at')
    list_filter = ('language', 'is_active')
    search_fields = ('key', 'alt', 'caption')
    ordering = ('key',)
    readonly_fields = ('_note', 'thumb')

    fieldsets = (
        (None, {'fields': ('key', 'language', 'image', 'alt', 'caption', 'is_active')}),
        ('Info', {'fields': ('thumb', '_note')}),
    )

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px;border-radius:6px;" />', obj.image.url)
        return '-'
    thumb.short_description = 'Preview'

    def _note(self, obj):
        return format_html(
            "<div style='color:#666'>"
            "Файл может быть оптимизирован/перекодирован в WEBP при сохранении. SVG не изменяется."
            "</div>"
        )
    _note.short_description = 'Note'
