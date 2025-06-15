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
            'secondary_background_color': forms.ColorInput(attrs={'class': 'color-preview'}),
            'secondary_text_color': forms.ColorInput(attrs={'class': 'color-preview'}),
            'text_color': forms.ColorInput(attrs={'class': 'color-preview'}),
            'border_color': forms.ColorInput(attrs={'class': 'color-preview'}),
        }
        
        color_fields = [
            'primary_color', 'primary_hover',
            'secondary_color', 'secondary_hover',
            'background_color', 'secondary_background_color',
            'secondary_text_color', 'text_color',
            'border_color', 'muted_text_color'
        ]

    class Media:
        js = ('admin/js/color_preview.js',)

