from django.contrib import admin
from .models import HotDealSection, HotDealItem


@admin.register(HotDealSection)
class HotDealSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "additional_description", "description")
    list_editable = ("additional_description", "description")
    

@admin.register(HotDealItem)
class HotDealItemAdmin(admin.ModelAdmin):
    list_display = ("section", "property", "is_active")
    list_editable = ("is_active",)
