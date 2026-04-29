"""
Views per l'app Chatbot.
Gestisce le API di chat e le interazioni con il motore AI.
"""
import logging
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ChatLog
from .serializers import ChatMessageSerializer, ChatResponseSerializer
from .ai_engine import generate_pharmacy_response

logger = logging.getLogger('chatbot')


@api_view(['POST'])
def chat_message(request):
    """
    POST /api/chat/
    
    Riceve un messaggio dall'utente e restituisce la risposta AI.
    
    Request Body:
        {
            "message": "Ho mal di testa",
            "session_id": "abc123" (opzionale)
        }
    
    Response:
        {
            "response": "Per il mal di testa...",
            "timestamp": "2024-01-15T10:30:00Z",
            "provider": "mock",
            "session_id": "abc123"
        }
    """
    serializer = ChatMessageSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {'error': 'Messaggio non valido', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_message = serializer.validated_data['message']
    session_id = serializer.validated_data.get('session_id')

    logger.info(f"Messaggio ricevuto: '{user_message[:100]}' | Session: {session_id}")

    try:
        # Genera risposta AI
        ai_result = generate_pharmacy_response(user_message)

        # Salva nel log
        chat_log = ChatLog.objects.create(
            user_message=user_message,
            bot_response=ai_result['response'],
            session_id=session_id,
            response_time_ms=ai_result['response_time_ms'],
            ai_provider=ai_result['provider'],
        )

        # Prepara risposta
        response_data = {
            'response': ai_result['response'],
            'timestamp': chat_log.timestamp.isoformat(),
            'provider': ai_result['provider'],
            'session_id': session_id,
        }

        response_serializer = ChatResponseSerializer(data=response_data)
        response_serializer.is_valid()

        logger.info(
            f"Risposta generata in {ai_result['response_time_ms']}ms "
            f"| Provider: {ai_result['provider']}"
        )

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Errore nella generazione della risposta: {e}")
        return Response(
            {'error': 'Errore interno del server. Riprovi più tardi.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def chat_history(request):
    """
    GET /api/chat/history/
    
    Restituisce la cronologia chat (per analytics / admin).
    Query params: ?session_id=abc123&limit=50
    """
    session_id = request.query_params.get('session_id')
    limit = min(int(request.query_params.get('limit', 50)), 100)

    queryset = ChatLog.objects.all()

    if session_id:
        queryset = queryset.filter(session_id=session_id)

    logs = queryset[:limit]

    data = [
        {
            'user_message': log.user_message,
            'bot_response': log.bot_response,
            'timestamp': log.timestamp.isoformat(),
            'provider': log.ai_provider,
        }
        for log in logs
    ]

    return Response({
        'count': len(data),
        'results': data,
    })
