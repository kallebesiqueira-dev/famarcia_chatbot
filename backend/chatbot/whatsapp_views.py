"""
Views per l'integrazione WhatsApp.
Genera link WhatsApp pre-formattati.
"""
import logging
from urllib.parse import quote
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import WhatsAppRequestSerializer

logger = logging.getLogger('chatbot')


def generate_whatsapp_url(message: str, phone_number: str = None) -> str:
    """
    Genera URL WhatsApp con messaggio pre-compilato.
    
    Args:
        message: Testo del messaggio
        phone_number: Numero di telefono (con prefisso internazionale, senza +)
        
    Returns:
        URL WhatsApp formattato
    """
    if not phone_number:
        phone_number = getattr(settings, 'WHATSAPP_DEFAULT_NUMBER', '393331234567')

    # Rimuovi caratteri non numerici dal numero
    phone_number = ''.join(filter(str.isdigit, phone_number))

    # Encode del messaggio per URL
    encoded_message = quote(message, safe='')

    return f"https://wa.me/{phone_number}?text={encoded_message}"


@api_view(['POST'])
def whatsapp_link(request):
    """
    POST /api/whatsapp/
    
    Genera un link WhatsApp con messaggio pre-compilato.
    
    Request Body:
        {
            "message": "Vorrei informazioni sulla disponibilità...",
            "phone_number": "393331234567" (opzionale)
        }
    
    Response:
        {
            "whatsapp_url": "https://wa.me/393331234567?text=...",
            "message": "Vorrei informazioni...",
            "phone_number": "393331234567"
        }
    """
    serializer = WhatsAppRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {'error': 'Dati non validi', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    message = serializer.validated_data['message']
    phone_number = serializer.validated_data.get(
        'phone_number',
        getattr(settings, 'WHATSAPP_DEFAULT_NUMBER', '393331234567')
    )

    whatsapp_url = generate_whatsapp_url(message, phone_number)

    logger.info(f"WhatsApp link generato per: {phone_number}")

    return Response({
        'whatsapp_url': whatsapp_url,
        'message': message,
        'phone_number': phone_number,
    }, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# PREDISPOSIZIONE FUTURA: Twilio / Meta WhatsApp Business API
# ---------------------------------------------------------------------------
#
# Per integrare Twilio WhatsApp:
#
# 1. pip install twilio
# 2. Configurare in settings.py:
#    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
#    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
#    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
#
# 3. Implementare:
#
# from twilio.rest import Client
#
# def send_whatsapp_message(to_number, message):
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     message = client.messages.create(
#         from_=f'whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}',
#         body=message,
#         to=f'whatsapp:+{to_number}'
#     )
#     return message.sid
#
# ---------------------------------------------------------------------------
