from django.contrib import admin
from .models import HotDealSection, HotDealItem


@admin.register(HotDealSection)
class HotDealSectionAdmin(admin.ModelAdmin):
    list_display = ("name","is_active","order")
    list_editable = ("is_active","order")
    

@admin.register(HotDealItem)
class HotDealItemAdmin(admin.ModelAdmin):
    list_display = ("section", "property", "is_active")
    list_editable = ("is_active",)
