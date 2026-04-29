"""Admin configuration per l'app Chatbot."""
from django.contrib import admin
from .models import ChatLog


@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ['user_message_short', 'bot_response_short', 'ai_provider', 'response_time_ms', 'timestamp']
    list_filter = ['ai_provider', 'timestamp']
    search_fields = ['user_message', 'bot_response']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']

    def user_message_short(self, obj):
        return obj.user_message[:80] + '...' if len(obj.user_message) > 80 else obj.user_message
    user_message_short.short_description = 'Messaggio Utente'

    def bot_response_short(self, obj):
        return obj.bot_response[:80] + '...' if len(obj.bot_response) > 80 else obj.bot_response
    bot_response_short.short_description = 'Risposta Bot'
