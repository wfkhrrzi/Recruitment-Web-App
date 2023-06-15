from django.urls import path

from main.consumers import WSResumeParserNotification

ws_urlpatterns = [
    path('notification/parser',WSResumeParserNotification.as_asgi())
]