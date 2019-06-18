from channels.auth import AuthMiddlewareStack
from device.token_auth import TokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
import device.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket':
    AuthMiddlewareStack(URLRouter(device.routing.device_urlpatterns)),
})
