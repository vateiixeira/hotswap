from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/sessoes/$', consumers.SessoesConsumer.as_asgi()),
    re_path(r'ws/socin/$', consumers.SocinConsumer.as_asgi()),
]