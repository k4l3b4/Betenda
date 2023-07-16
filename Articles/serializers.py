from Users.serializers import User_CUD_Serializer
from betenda_api.methods import get_reactions
from rest_framework import serializers
from .models import Article


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
            'slug': {'read_only': True},
            'body': {'write_only': True},
            'published_date': {'read_only': True},
            'modified_date': {'read_only': True},
        }

    def create(self, validated_data):
        authors = validated_data.pop("authors", [])
        instance = super().create(validated_data)
        for author in authors:
            instance.authors.add(author)
        return instance

    def update(self, instance, validated_data):
        authors = validated_data.pop("authors", [])
        instance = super().update(instance, validated_data)
        for author in authors:
            instance.authors.add(author)
        return instance


class ArticleGetSerializer(serializers.ModelSerializer):
    authors = User_CUD_Serializer(many=True, read_only=True)
    reactions = serializers.SerializerMethodField()

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
            'reactions'
        ]

    def get_reactions(self, obj):
        return get_reactions(self, obj)
