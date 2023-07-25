from Users.serializers import User_SIMPLE_Serializer
from .models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    user = User_SIMPLE_Serializer()
    class Meta:
        model = Notification
        fields = [
            'id',
            'message',
            'user',
            'message_type',
            'is_read',
            'created_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'created_at': {'read_only': True},
        }