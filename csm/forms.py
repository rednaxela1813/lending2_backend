from django import forms
from .models import SiteTheme



class SiteThemeForm(forms.ModelForm):
    class Meta:
        model = SiteTheme
        fields = '__all__'
        widgets = {
            'primary_color': forms.ColorInput(attrs={'class': 'color-preview'}),
            'primary_hover': forms.ColorInput(attrs={'class': 'color-preview'}),
            'secondary_color': forms.ColorInput(attrs={'class': 'color-preview'}),
            'secondary_hover': forms.ColorInput(attrs={'class': 'color-preview'}),
            'background_color': forms.ColorInput(attrs={'class': 'color-preview'}),
            'text_color': forms.ColorInput(attrs={'class': 'color-preview'}),
            'border_color': forms.ColorInput(attrs={'class': 'color-preview'}),
        }

    class Media:
        js = ('admin/js/color_preview.js',)

