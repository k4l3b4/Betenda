from django.urls import re_path
from Comments.consumers import CommentConsumer
from Notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/comment/$', CommentConsumer.as_asgi(), name="comments_create_update_delete_consumer"),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi(), name="notifications_get_read_consumer"),
]