# apps/company/admin.py
from django.contrib import admin
from .models import CompanyInfo, FooterInfo, OpeningHour, SpecialOpening

class OpeningHourInline(admin.TabularInline):
    model = OpeningHour
    extra = 1
    ordering = ("weekday", "start_time")
    fields = ("weekday", "start_time", "end_time")

class SpecialOpeningInline(admin.TabularInline):
    model = SpecialOpening
    extra = 0
    fields = ("date", "is_closed", "start_time", "end_time", "note")

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email", "phone", "address")
    inlines = [OpeningHourInline, SpecialOpeningInline]

@admin.register(FooterInfo)
class FooterInfoAdmin(admin.ModelAdmin):
    list_display = ("company", "about_title", "updated_at")
    autocomplete_fields = ("company",)
