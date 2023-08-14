from .models import BookMark
from rest_framework import serializers


class BookMarkSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    poem = serializers.SerializerMethodField()

    class Meta:
        model = BookMark
        fields = [
            'id',
            'article',
            'post',
            'poem',
            'added_date',
        ]

    def get_article(self):
        pass
    def get_post(self):
        pass
    def get_poem(self):
        pass