"""
ASGI config for recruitment project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
settings_module = "recruitment.prod_settings" if 'WEBSITE_HOSTNAME' in os.environ else 'recruitment.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

from django.core.asgi import get_asgi_application
django_asgi_application = get_asgi_application()

from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import django_eventstream
from main.ws_urls import ws_urlpatterns

application = ProtocolTypeRouter({
    'http': URLRouter([
        path(
            'notification/parser', 
            AuthMiddlewareStack(URLRouter(django_eventstream.routing.urlpatterns)), 
            { 'channels': ['resume_parser'] }
        ),
        path(
            'notification/upload', 
            AuthMiddlewareStack(URLRouter(django_eventstream.routing.urlpatterns)), 
            { 'channels': ['resume_upload'] }
        ),
        re_path(r'', django_asgi_application),
    ]),

    'websocket':AuthMiddlewareStack(URLRouter(ws_urlpatterns))

})
