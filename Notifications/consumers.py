from betenda_api.methods import mark_notification_as_read
from .serializers import NotificationSerializer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
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
        notification_data = event.get("object")
        if notification_data:
            notification_json = json.dumps(notification_data, cls=DjangoJSONEncoder)
            await self.send(text_data=notification_json)

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        notification_id = message.get("ids")

        if notification_id:
            try:
                ids = [int(id_str) for id_str in notification_id.split(',')]
                mark_notification_as_read(ids)
            except:
                await self.send(text_data="An error occurred")
