from Reactions.models import Reaction, ReactionCount
from betenda_api.methods import get_reactions
from rest_framework.fields import MaxLengthValidator
from rest_framework import serializers
from Posts.models import Post
from Users.serializers import User_CUD_Serializer
from django.contrib.contenttypes.models import ContentType


class Post_CUD_Serializer(serializers.ModelSerializer):
    user = User_CUD_Serializer(read_only=True)
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'parent',
            'slug',
            'media',
            'media_type',
            'user',
            'reactions',
            'created_at',
            'edited_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True, 'allow_null': True},
            'slug': {'read_only': True, 'allow_null': True},
            'content': {'validators': [MaxLengthValidator(300)]},
            'created_at': {'read_only': True, 'allow_null': True},
            'edited_at': {'read_only': True, 'allow_null': True},
        }

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def get_reactions(self, obj):
        return get_reactions(self, obj)