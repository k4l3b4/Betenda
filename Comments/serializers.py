from django.db.models import Count
from Users.serializers import User_SIMPLE_Serializer
from betenda_api.methods import get_reactions_method
from rest_framework import serializers
from .models import Comment


class Comment_CUD_Serializer(serializers.ModelSerializer):
    user = User_SIMPLE_Serializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
            'user',
            'parent',
            'immediate_parent',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'id':{'read_only':True},
            'created_at':{'read_only':True},
            'updated_at':{'read_only':True},
        }

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class Comment_GET_Serializer(serializers.ModelSerializer):
    user = User_SIMPLE_Serializer()
    reactions = serializers.SerializerMethodField()
    reply_to = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
            'user',
            'parent',
            'immediate_parent',
            'reply_to',
            'reply_count',
            'reactions',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'id':{'read_only':True},
            'user':{'read_only':True},
            'parent':{'read_only':True},
            'immediate_parent':{'read_only':True},
            'reactions':{'read_only':True},
            'created_at':{'read_only':True},
            'updated_at':{'read_only':True},
        }

    def get_reactions(self, obj):
        return get_reactions_method(self, obj)
    
    def get_commenter(self, comment):
        return comment.user.user_name if comment.user else None
    
    def get_reply_to(self, obj):
        # Check if the comment has an immediate parent and that it is not a first level reply
        if obj.immediate_parent and obj.immediate_parent != obj.parent:
            return self.get_commenter(obj.immediate_parent)
        else:
            return None
        
    def get_reply_count(self, obj):
        # Check if the comment has any replies
        return Comment.objects.filter(parent=obj.id).count()

class Comment_Notification_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
        ]