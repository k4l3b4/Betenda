from django.urls import re_path
from Notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi(), name="notifications_get_read_consumer"),
]