from django.conf.urls import url

from room.consumers import KuropolyConsumer

websocket_urlpatterns = [
    url(r'^ws/play/(?P<idRoom>\w+)/$', KuropolyConsumer.as_asgi()),
]