# properties/admin.py

from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    readonly_fields = ('preview',)  # 👈 показываем превью как read-only
    fields = ('image', 'description', 'preview')  # порядок отображения



@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('name', 'type', 'location', 'created_at')
