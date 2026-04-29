"""
Modelli per l'app Chatbot.
Gestisce il logging delle conversazioni utente-bot.
"""
from django.db import models


class ChatLog(models.Model):
    """
    Log delle conversazioni tra utente e assistente AI.
    Memorizza ogni scambio per analytics e miglioramento del servizio.
    """
    user_message = models.TextField(
        verbose_name='Messaggio Utente',
        help_text='Il messaggio inviato dall\'utente'
    )
    bot_response = models.TextField(
        verbose_name='Risposta Bot',
        help_text='La risposta generata dall\'assistente AI'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data e Ora',
        db_index=True
    )
    # Campi predisposti per autenticazione futura
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ID Sessione',
        help_text='Identificativo sessione utente (futuro)'
    )
    # Metadata per analytics
    response_time_ms = models.IntegerField(
        default=0,
        verbose_name='Tempo Risposta (ms)',
        help_text='Tempo impiegato per generare la risposta'
    )
    ai_provider = models.CharField(
        max_length=50,
        default='mock',
        verbose_name='Provider AI',
        help_text='Il provider AI utilizzato (mock, openai, etc.)'
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Log Chat'
        verbose_name_plural = 'Log Chat'
        indexes = [
            models.Index(fields=['session_id', 'timestamp']),
        ]

    def __str__(self):
        return f"[{self.timestamp:%d/%m/%Y %H:%M}] {self.user_message[:50]}..."
