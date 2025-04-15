from django.contrib import admin
from .models import HeroSection, HeaderSection, FooterInfo, CompanyInfo


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')

@admin.register(HeaderSection)
class HeaderSectionAdmin(admin.ModelAdmin):
    list_display = ('logo_text', 'nav_services', 'nav_why', 'nav_contact', 'button_text', 'updated_at')
    

admin.site.register(FooterInfo)
admin.site.register(CompanyInfo)
