from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HeroSection, HeaderSection, FooterInfo, CompanyInfo
from .serializers import HeroSectionSerializer, HeaderSectionSerializer, FooterInfoSerializer, CompanyInfoSerializer, ContactRequestSerializer
from rest_framework.generics import RetrieveAPIView
from core.utils.telegram import send_telegram_message


from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from decouple import config
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

import requests

import logging


class HeroSectionView(APIView):
    def get(self, request):
        hero = HeroSection.objects.first()
        serializer = HeroSectionSerializer(hero)
        return Response(serializer.data)


class HeaderSectionView(RetrieveAPIView):
    queryset = HeaderSection.objects.all()
    serializer_class = HeaderSectionSerializer

    def get_object(self):
        return HeaderSection.objects.first()
    

class FooterInfoView(APIView):
    def get(self, request):
        footer = FooterInfo.objects.last()
        serializer = FooterInfoSerializer(footer)
        return Response(serializer.data)


class CompanyInfoView(APIView):
    def get(self, request):
        info = CompanyInfo.objects.first()
        serializer = CompanyInfoSerializer(info)
        return Response(serializer.data)
    

# class ContactFormView(APIView):
#     def post(self, request):
#         data = request.data
#         name = data.get("name")
#         contact = data.get("contact")
#         message = data.get("message")

#         if not name or not contact:
#             return Response({"error": "Missing required fields"}, status=400)

#         text = f"📩 <b>Новая заявка</b>\n\n👤 Имя: {name}\n📞 Контакт: {contact}\n💬 Сообщение: {message or '-'}"

#         success = send_telegram_message(text)

#         return Response({"success": success}, status=status.HTTP_200_OK if success else 500)
    
    


# import os






logger = logging.getLogger(__name__)


TELEGRAM_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID
ALLOWED_ORIGINS = settings.ALLOWED_ORIGINS

@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='dispatch')
class ContactRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        origin = request.META.get("HTTP_ORIGIN", "")
        if origin not in ALLOWED_ORIGINS:
            logger.warning(f"Blocked origin: {origin}")
            return JsonResponse({"error": "Invalid origin"}, status=403)

        serializer = ContactRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning("Invalid form submission")
            return JsonResponse(serializer.errors, status=400)

        # Honeypot check
        if request.data.get("honeypot"):
            logger.warning("Bot detected via honeypot")
            return JsonResponse({"error": "Suspicious activity"}, status=400)

        name = serializer.validated_data["name"]
        contact = serializer.validated_data["contact"]
        message = serializer.validated_data["message"]

        # Content validation
        if any(s in message.lower() for s in ["http://", "https://", "<script>"]):
            logger.warning("Potential spam detected in message")
            return JsonResponse({"error": "Invalid content"}, status=400)

        text = f"📩 *Nová žiadosť z formulára:*\n\n👤 *Meno:* {name}\n📞 *Kontakt:* {contact}\n💬 *Správa:*\n{message}"

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(telegram_url, json=payload)
            response.raise_for_status()
            logger.info(f"Message sent to Telegram from {name}")
        except requests.RequestException as e:
            logger.error(f"Failed to send message to Telegram: {e}")
            return JsonResponse({"error": "Failed to send message"}, status=500)

        return JsonResponse({"success": "Message sent"})
