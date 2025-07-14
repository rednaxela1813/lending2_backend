from django.contrib import admin
from .models import HeroSection, HeaderSection, FooterInfo, CompanyInfo, SiteTheme, FrontendTheme
from .forms import SiteThemeForm, FrontendThemeForm


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at', 'button_text', 'right_colon_text')

@admin.register(HeaderSection)
class HeaderSectionAdmin(admin.ModelAdmin):
    list_display = ('logo_text', 'nav_services', 'nav_why', 'nav_contact', 'button_text', 'updated_at')
    
    


@admin.register(FrontendTheme)
class FrontendThemeAdmin(admin.ModelAdmin):
    form = FrontendThemeForm
        

@admin.register(SiteTheme)
class SiteThemeAdmin(admin.ModelAdmin):
    form = SiteThemeForm
    

admin.site.register(FooterInfo)
admin.site.register(CompanyInfo)
