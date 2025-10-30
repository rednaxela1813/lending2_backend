from django import forms
from .models import  FrontendTheme



# class SiteThemeForm(forms.ModelForm):
#     class Meta:
#         model = SiteTheme
#         fields = '__all__'
#         widgets = {
#             'primary_color': forms.ColorInput(attrs={'class': 'color-preview'}),
#             'primary_hover': forms.ColorInput(attrs={'class': 'color-preview'}),
#             'secondary_color': forms.ColorInput(attrs={'class': 'color-preview'}),
#             'secondary_hover': forms.ColorInput(attrs={'class': 'color-preview'}),
#             'background_color': forms.ColorInput(attrs={'class': 'color-preview'}),
#             'secondary_background_color': forms.ColorInput(attrs={'class': 'color-preview'}),
#             'secondary_text_color': forms.ColorInput(attrs={'class': 'color-preview'}),
#             'text_color': forms.ColorInput(attrs={'class': 'color-preview'}),
#             'border_color': forms.ColorInput(attrs={'class': 'color-preview'}),
#         }
        
#         color_fields = [
#             'primary_color', 'primary_hover',
#             'secondary_color', 'secondary_hover',
#             'background_color', 'secondary_background_color',
#             'secondary_text_color', 'text_color',
#             'border_color', 'muted_text_color'
#         ]

#     class Media:
#         js = ('admin/js/color_preview.js',)

class FrontendThemeForm(forms.ModelForm):
    class Meta:
        model = FrontendTheme
        fields = '__all__'
        widgets = {
            'navbar_background': forms.TextInput(attrs={'type': 'color', 'class': 'color-preview'}),
            'body_background': forms.TextInput(attrs={'type': 'color', 'class': 'color-preview'}),
            'footer_background': forms.TextInput(attrs={'type': 'color', 'class': 'color-preview'}),
            'text_color': forms.TextInput(attrs={'type': 'color', 'class': 'color-preview'}),
            'text_hover_color': forms.TextInput(attrs={'type': 'color', 'class': 'color-preview'}),
            'border_color': forms.TextInput(attrs={'type': 'color', 'class': 'color-preview'}),
            'border_hover_color': forms.TextInput(attrs={'type': 'color', 'class': 'color-preview'}),
            'primary_color': forms.TextInput(attrs={'type': 'color', 'class': 'color-preview'}),
            'primary_hover_color': forms.TextInput(attrs={'type': 'color', 'class': 'color-preview'}),
        }

    class Media:
        js = ('js/color_preview.js',)
        
        
        
class ContactRequestForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
    "class": "block w-full min-w-0 flex-1 rounded-none rounded-e-lg border border-border bg-navbar p-2.5 text-sm text-text focus:border-primary focus:ring-primary",
    "placeholder": " Vaše Meno"
})
    )
    contact = forms.EmailField(
        max_length=255,
        error_messages={
            'invalid': 'Zadajte platný e-mail.',
            'required': 'Toto pole je povinné.'
        },
        widget=forms.TextInput(attrs={
            "class": "block w-full rounded-lg border border-border bg-navbar p-2.5 ps-12 text-sm text-text focus:border-primary focus:ring-primary",
            "placeholder": " your@email.com"
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "block w-full rounded-lg border border-border bg-navbar p-2.5 text-sm text-text focus:border-primary focus:ring-primary",
            "placeholder": "Leave a comment...",
            "rows": 4
        })
    )
    consent = forms.BooleanField(
    required=True,
    widget=forms.CheckboxInput(attrs={
        "id": "consent",  # для JS
        "class": "h-4 w-4 rounded-sm border-border bg-gray-100 text-primary focus:ring-2 focus:ring-primary dark:bg-secondary dark:focus:ring-primary"
    })
)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)