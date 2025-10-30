from django.contrib import admin
from .models import HeroSection, HeaderSection, FooterInfo, CompanyInfo,  FrontendTheme, ServiceSection, CarouselImage, HotDealItem, HotDealSection, Icon, BottomCTASection
from .forms import  FrontendThemeForm
from django import forms
from django.contrib.admin.widgets import AdminDateWidget




    
    
@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at', 'button_text', 'right_colon_text')

@admin.register(HeaderSection)
class HeaderSectionAdmin(admin.ModelAdmin):
    list_display = ('logo_text', 'nav_services', 'nav_why', 'nav_contact', 'button_text', 'updated_at')
    
    


@admin.register(FrontendTheme)
class FrontendThemeAdmin(admin.ModelAdmin):
    form = FrontendThemeForm
        
        
@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('updated_at',)

# @admin.register(SiteTheme)
# class SiteThemeAdmin(admin.ModelAdmin):
#     form = SiteThemeForm
    

admin.site.register(FooterInfo)
admin.site.register(CompanyInfo)
admin.site.register(CarouselImage)
admin.site.register(HotDealItem)
admin.site.register(HotDealSection)
admin.site.register(Icon)
admin.site.register(BottomCTASection)




