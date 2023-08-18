from BookMarks.models import BookMark
from betenda_api.methods import get_reactions_method, get_replies_count, get_bookmarked_method, BadRequest
from rest_framework.fields import MaxLengthValidator
from rest_framework import serializers
from Posts.models import Post
from Users.serializers import User_CD_Serializer
from django.contrib.contenttypes.models import ContentType

class Thread_CUD_Serializer(serializers.ModelSerializer):
    '''
    Couldn't be bothered with trying to fix infinite nesting so using this serializer for the threads instead
    '''
    parent = serializers.IntegerField(source="parent_id")
    user = User_CD_Serializer(read_only=True)
    reactions = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'slug',
            'media',
            'parent',
            'media_type',
            'replies_count',
            'user',
            'reactions',
            'bookmarked',
            'created_at',
            'edited_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True, 'allow_null': True},
            'slug': {'read_only': True, 'allow_null': True},
            'content': {'validators': [MaxLengthValidator(300)]},
            'replies_count': {'read_only': True},
            'parent': {'read_only': True},
            'created_at': {'read_only': True, 'allow_null': True},
            'edited_at': {'read_only': True, 'allow_null': True},
        }
        
    
    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def get_reactions(self, obj):
        return get_reactions_method(self, obj)

    def get_replies_count(self, obj):
        return get_replies_count(self, obj)
    
    def get_bookmarked(self, obj):
        return get_bookmarked_method(self, obj)

class Post_CUD_Serializer(serializers.ModelSerializer):
    user = User_CD_Serializer(read_only=True)
    reactions = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()
    thread = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'slug',
            'media',
            'parent',
            'media_type',
            'user',
            'replies_count',
            'reactions',
            'bookmarked',
            'thread',
            'created_at',
            'edited_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True, 'allow_null': True},
            'slug': {'read_only': True, 'allow_null': True},
            'parent': {'read_only': True},
            'content': {'validators': [MaxLengthValidator(300)]},
            'created_at': {'read_only': True, 'allow_null': True},
            'edited_at': {'read_only': True, 'allow_null': True},
        }

    def validate_media(self, value):
        # List of allowed media file extensions
        allowed_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'mp4', 'mkv']

        # Get the file extension from the uploaded file
        if value:
            file_extension = value.name.split('.')[-1]
            if file_extension.lower() not in allowed_extensions:
                raise BadRequest("Unsupported file type")

        return value

    
    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def get_reactions(self, obj):
        return get_reactions_method(self, obj)

    def get_replies_count(self, obj):
        return get_replies_count(self, obj)   
    
    def get_bookmarked(self, obj):
        return get_bookmarked_method(self, obj)

    def get_thread(self, obj):
        request = self.context.get('request')
        if request is None:
            return []  # No request object, return an empty list

        # Filter and limit the replies for each parent post
        replies = Post.objects.filter(parent_id=obj.id, user=obj.user)[:5]

        # Serialize the replies, passing the request context to the CommentSerializer
        serializer = Thread_CUD_Serializer(replies, many=True, context={'request': request})
        return serializer.data
    



class Post_Notification_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'slug',
            'media',
            'media_type',
        ]