from Users.serializers import User_CUD_Serializer
from Comments.models import Comment
from betenda_api.methods import get_reactions_method
from rest_framework import serializers
from .models import Article
from django.contrib.contenttypes.models import ContentType

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'desc',
            'body',
            'image',
            'authors',
            'status',
            'featured',
            'published_date',
            'modified_date',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'authors': {'allow_null': True},
            'slug': {'read_only': True},
            'body': {'write_only': True},
            'published_date': {'read_only': True},
            'modified_date': {'read_only': True},
        }

    def create(self, validated_data):
        authors = validated_data.pop("authors", [])
        instance = super().create(validated_data)
        # adding the authors
        for author in authors:
            instance.authors.add(author)
        return instance

    def update(self, instance, validated_data):
        authors = validated_data.pop("authors", [])
        instance = super().update(instance, validated_data)
        # adding the authors, duplicates will be replaced
        for author in authors:
            instance.authors.add(author)
        return instance


class ArticleGetSerializer(serializers.ModelSerializer):
    authors = User_CUD_Serializer(many=True, read_only=True)
    reactions = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'desc',
            'body',
            'image',
            'authors',
            'status',
            'comments_count',
            'featured',
            'published_date',
            'modified_date',
            'reactions'
        ]

    def get_reactions(self, obj):
        return get_reactions_method(self, obj)
    
    def get_comments_count(self, obj):
        '''
        takes in context and obj to retrieve reactions for the specific objects
        '''
        comments_count = 0    
        content_type = ContentType.objects.get_for_model(obj)

        comments_count = Comment.objects.filter(
            content_type=content_type, object_id=obj.id).count()

        return comments_count


# same serializer with only the body omitted since it will be to big to just leave it when unused
class ArticleListSerializer(serializers.ModelSerializer):
    authors = User_CUD_Serializer(many=True, read_only=True)
    reactions = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'desc',
            'image',
            'authors',
            'status',
            'comments_count',
            'featured',
            'published_date',
            'modified_date',
            'reactions'
        ]

    def get_reactions(self, obj):
        return get_reactions_method(self, obj)
    
    def get_comments_count(self, obj):
        '''
        takes in context and obj to retrieve reactions for the specific objects
        '''
        comments_count = 0    
        content_type = ContentType.objects.get_for_model(obj)

        comments_count = Comment.objects.filter(
            content_type=content_type, object_id=obj.id).count()

        return comments_count
    


class Article_Notification_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'image',
            'status',
        ]