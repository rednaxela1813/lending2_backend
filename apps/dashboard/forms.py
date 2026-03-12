from django import forms
from .models import EditableText, EditableImage, SiteSlot

base_input = {"class":"block w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"}

class EditableTextForm(forms.ModelForm):
    class Meta:
        model = EditableText
        fields = ("slot","key","language","title","text","is_active")
        widgets = {
            "slot": forms.Select(attrs=base_input),
            "key": forms.TextInput(attrs=base_input|{"placeholder":"(auto from slot)"}),
            "title": forms.TextInput(attrs=base_input),
            "text": forms.Textarea(attrs={"class":base_input["class"],"rows":8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # показываем только текстовые слоты
        self.fields["slot"].queryset = SiteSlot.objects.filter(kind=SiteSlot.TEXT)



class EditableImageForm(forms.ModelForm):
    class Meta:
        model = EditableImage
        # ⚠️ только существующие поля модели!
        fields = ["key", "image", "alt", "caption", "is_active", "company"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)