from Users.serializers import User_CUD_Serializer
from .models import Comment
from rest_framework import serializers


class Comment_CUD_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'comment',
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class Comment_GET_Serializer(serializers.ModelSerializer):
    user = User_CUD_Serializer()

    class Meta:
        model = Comment
        fields = [
            'user',
            'comment',
            'created_at',
            'updated_at',
        ]
