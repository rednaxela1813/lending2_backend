from rest_framework import serializers
from .models import HeroSection, HeaderSection, FooterInfo, CompanyInfo, ContactRequest

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