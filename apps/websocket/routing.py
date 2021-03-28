from django.conf.urls import url

from apps.websocket.consumers import KuropolyConsumer

websocket_urlpatterns = [
    url(r'^wss/play/(?P<idRoom>\w+)/$', KuropolyConsumer.as_asgi()),
]