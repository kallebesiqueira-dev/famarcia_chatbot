"""
URL Configuration principale del progetto Farmacia Chatbot.
Tutte le API sono organizzate sotto /api/ con namespace separati.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """Endpoint radice dell'API - mostra le rotte disponibili."""
    return JsonResponse({
        'message': 'Farmacia AI Chatbot API',
        'version': '1.0.0',
        'endpoints': {
            'chat': '/api/chat/',
            'products': '/api/products/',
            'whatsapp': '/api/whatsapp/',
            'admin': '/admin/',
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/chat/', include('chatbot.urls')),
    path('api/products/', include('pharmacy.urls')),
    path('api/whatsapp/', include('chatbot.whatsapp_urls')),
]
