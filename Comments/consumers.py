from urllib.parse import parse_qs
from Comments.models import Comment
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve the resource ID and resource type from query parameters
        params = self.scope['query_string'].decode()
        query_params = parse_qs(params)

        self.resource_id = query_params['resource_id'][0]
        self.resource_type = query_params['resource_type'][0]
        self.parent_id = query_params.get('parent_id', [None])[0]
        user_id = self.scope["user"].id
        # Create a group name based on the resource ID and resource type
        self.group_name = f'comment_{self.resource_type}_{self.resource_id}_{str(user_id)}'

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        # Process incoming WebSocket messages
        data = json.loads(text_data)

        if 'comment_id' in data:
            # Update an existing comment
            comment_id = data['comment_id']
            try:
                comment = Comment.objects.get(id=comment_id)
                # Only update the specified fields
                if 'content' in data:
                    comment.content = data['content']
                # Save the updated comment
                comment.save()
            except Comment.DoesNotExist:
                # Handle the case when the comment does not exist
                pass
        else:
            comment = Comment.objects.create(
                resource_id=self.resource_id,
                resource_type=self.resource_type,
                parent_id=self.parent_id,
                content=data['content']
            )

        # Prepare the response data with the comment details
        response_data = {
            'comment_id': comment.id,
            'content': comment.content,
        }

        # Include the parent ID in the response if it is present
        if self.parent_id:
            response_data['parent_id'] = self.parent_id

        # Broadcast the new comment to all WebSocket connections in the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'comment_message',
                'data': response_data,
            }
        )

    async def comment_message(self, event):
        # Send the comment message to the WebSocket connection
        await self.send(json.dumps({
            'comment_id': event['comment_id'],
            'content': event['content']
        }))