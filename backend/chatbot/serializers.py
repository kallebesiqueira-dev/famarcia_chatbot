"""
Serializer per l'app Chatbot.
"""
from rest_framework import serializers
from .models import ChatLog


class ChatMessageSerializer(serializers.Serializer):
    """Serializer per i messaggi in ingresso dall'utente."""
    message = serializers.CharField(
        max_length=2000,
        help_text='Messaggio dell\'utente',
        required=True,
    )
    session_id = serializers.CharField(
        max_length=255,
        required=False,
        help_text='ID sessione utente (opzionale)'
    )


class ChatResponseSerializer(serializers.Serializer):
    """Serializer per le risposte del bot."""
    response = serializers.CharField()
    timestamp = serializers.DateTimeField()
    provider = serializers.CharField()
    session_id = serializers.CharField(allow_null=True)


class ChatLogSerializer(serializers.ModelSerializer):
    """Serializer per il log delle chat (admin/analytics)."""
    class Meta:
        model = ChatLog
        fields = '__all__'
        read_only_fields = ['timestamp']


class WhatsAppRequestSerializer(serializers.Serializer):
    """Serializer per la richiesta di link WhatsApp."""
    message = serializers.CharField(
        max_length=2000,
        help_text='Messaggio da inviare su WhatsApp'
    )
    phone_number = serializers.CharField(
        max_length=20,
        required=False,
        help_text='Numero WhatsApp destinatario (opzionale, usa default)'
    )


class WhatsAppResponseSerializer(serializers.Serializer):
    """Serializer per la risposta con link WhatsApp."""
    whatsapp_url = serializers.URLField()
    message = serializers.CharField()
    phone_number = serializers.CharField()
