from django import forms
from .models import EditableText, EditableImage


class EditableTextForm(forms.ModelForm):
    class Meta:
        model = EditableText
        fields = ("key", "language", "title", "text", "is_active")
        widgets = {
            "key": forms.TextInput(attrs={"class": "input", "placeholder": "hero.title"}),
            "title": forms.TextInput(attrs={"class": "input"}),
            "text": forms.Textarea(attrs={"class": "textarea", "rows": 8}),
        }

class EditableImageForm(forms.ModelForm):
    class Meta:
        model = EditableImage
        fields = ("key", "language", "image", "alt", "caption", "is_active")
        widgets = {
            "key": forms.TextInput(attrs={"class": "input", "placeholder": "hero.image"}),
            "alt": forms.TextInput(attrs={"class": "input"}),
            "caption": forms.TextInput(attrs={"class": "input"}),
        }
