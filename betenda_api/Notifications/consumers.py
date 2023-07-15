from Notifications.models import Notification
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user_id = self.scope["user"].id
        await self.channel_layer.group_add(str(user_id), self.channel_name)

    async def disconnect(self, close_code):
        user_id = self.scope["user"].id
        await self.channel_layer.group_discard(str(user_id), self.channel_name)

    async def notify(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        notification_id = message.get("notification_id")

        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id)
                notification.mark_as_read()
            except:
                await self.send(text_data="An error occurred")