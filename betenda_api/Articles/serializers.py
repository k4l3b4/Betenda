from rest_framework.serializers import Serializer
from .models import Article


class ArticleSerializer(Serializer.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title',
            'desc',
            'body',
            'image',
            'authors',
            'status',
            'featured',
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)