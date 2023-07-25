from Notifications.models import Notification
from .serializers import NotificationSerializer
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user_id = self.scope["user"].id
        self.group_name = f'notification_{str(user_id)}'

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.send(text_data=json.dumps("Notifications socket connection established!"))

    async def disconnect(self, close_code):
        user_id = self.scope["user"].id
        await self.channel_layer.group_discard(f'notification_{str(user_id)}', self.channel_name)

    async def notify(self, event):
        notification_data = event.get("object")  # Access the "object" key from the event data
        if notification_data:
            serializer = NotificationSerializer(notification_data)
            notification_json = serializer.data
        await self.send(text_data=json.dumps(notification_json))

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        notification_id = message.get("notification_id")

        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id)
                notification.mark_as_read()
            except:
                await self.send(text_data="An error occurred")
