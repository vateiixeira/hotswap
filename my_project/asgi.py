
from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler

from my_project.ws import routing

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
    # "channel": ChannelNameRouter({
    #     "henry": HenryHandle.as_asgi(),
    #     "topdata": TopdataHandle.as_asgi(),
    # }),
})