from rest_framework import serializers
from .models import HeroSection, HeaderSection, FooterInfo, CompanyInfo, ContactRequest, SiteTheme

class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = '__all__'
 

class HeaderSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderSection
        fields = '__all__'


class FooterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterInfo
        fields = '__all__'


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = '__all__'
        
    
class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['name', 'contact', 'message']
        
        
# core/csm/serializers.py

class SiteThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteTheme
        fields = [
            'name',
            'primary_color',
            'primary_hover',
            'secondary_color',
            'secondary_hover',
            'background_color',
            'secondary_background_color',
            
            'text_color',
            'secondary_text_color',
            'border_color',
            'muted_text_color',
            'is_active',
        ]

        
    