from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from irnuscrawler_app.consumers import DownloadConsumer

websocket_urlpatterns = [
  path('ws/download/', DownloadConsumer.as_asgi()),
]