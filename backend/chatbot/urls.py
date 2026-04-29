"""URL patterns per l'app Chatbot."""
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_message, name='chat-message'),
    path('history/', views.chat_history, name='chat-history'),
]
