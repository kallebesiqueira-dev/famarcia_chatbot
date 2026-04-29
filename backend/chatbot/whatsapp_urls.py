"""URL patterns per WhatsApp."""
from django.urls import path
from . import whatsapp_views

app_name = 'whatsapp'

urlpatterns = [
    path('', whatsapp_views.whatsapp_link, name='whatsapp-link'),
]
