from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.urls import reverse, NoReverseMatch

class ResolvingLoginView(LoginView):
    """
    Поддерживает LOGIN_REDIRECT_URL как путь ('/dashboard/') и как имя ('dashboard:home').
    """
    def get_success_url(self):
        url = super().get_success_url()  # берёт settings.LOGIN_REDIRECT_URL или next
        if not url:
            return url
        # If it's already an absolute/relative path, return it as is.
        if url.startswith("/") or url.startswith("http"):
            return url
        # Otherwise, try to interpret it as a urlpattern name
        try:
            return reverse(url)
        except NoReverseMatch:
            return url
