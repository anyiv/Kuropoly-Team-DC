from django.conf.urls import re_path

from apps.websocket.consumers import KuropolyConsumer

websocket_urlpatterns = [
    re_path(r'^ws/play/(?P<idRoom>\w+)/$', KuropolyConsumer.as_asgi()),
]