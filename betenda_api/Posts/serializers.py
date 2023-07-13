from rest_framework import serializers

from Posts.models import Post
from Users.serializers import User_CUD_Serializer


class Post_CUD_Serializer(serializers.ModelSerializer):
    user = User_CUD_Serializer()

    class Meta:
        model = Post
        fields = [
            'user',
            'content',
            'parent',
            'slug',
            'media',
            'media_type',
            'created_at',
            'edited_at',
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'parent': {'read_only': True},
            'slug': {'read_only': True},
            'created_at': {'read_only': True},
            'edited_at': {'read_only': True},
        }

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
