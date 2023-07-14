from Users.models import User
from Users.serializers import User_CUD_Serializer
from rest_framework import serializers
from .models import Article



class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = [
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
            'slug': {'read_only': True},
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
