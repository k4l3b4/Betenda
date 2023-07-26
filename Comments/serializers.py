from betenda_api.methods import get_reactions_method
from rest_framework import serializers
from Users.serializers import User_CUD_Serializer
from .models import Comment


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
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
            'user',
            'parent_id',
            'reactions',
            'created_at',
            'updated_at',
        ]

    def get_reactions(self, obj):
        return get_reactions_method(self, obj)