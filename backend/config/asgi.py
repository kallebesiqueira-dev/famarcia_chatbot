"""
ASGI config for Farmacia Chatbot project.
Predisposto per WebSocket (futura integrazione real-time).
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_asgi_application()
