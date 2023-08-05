from Users.serializers import User_SIMPLE_Serializer
from Posts.serializers import Post_Notification_Serializer
from Articles.serializers import Article_Notification_Serializer
from Comments.serializers import Comment_Notification_Serializer
from Contributions.serializers import Poem_Notification_Serializer
from .models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    user = User_SIMPLE_Serializer()
    sender = User_SIMPLE_Serializer()
    post = Post_Notification_Serializer()
    article = Article_Notification_Serializer()
    poem = Poem_Notification_Serializer()
    comment = Comment_Notification_Serializer()

    class Meta:
        model = Notification
        fields = [
            'id',
            'message',
            'user',
            'sender',
            'post',
            'article',
            'poem',
            'comment',
            'message_type',
            'is_read',
            'created_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'created_at': {'read_only': True},
        }