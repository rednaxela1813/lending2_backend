from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Meno",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Vaše meno"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Váš email"})
    )
    message = forms.CharField(
        label="Správa",
        widget=forms.Textarea(attrs={"placeholder": "Vaša správa"})
    )
    consent = forms.BooleanField(
        label="Súhlasím so spracovaním osobných údajov",
        required=True
    )
