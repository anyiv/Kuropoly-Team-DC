from channels.routing import ProtocolTypeRouter, URLRouter
import apps.websocket.routing


application = ProtocolTypeRouter({
    'websocket': URLRouter(
        apps.websocket.routing.websocket_urlpatterns
        ),
})