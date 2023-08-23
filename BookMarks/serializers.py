from Articles.serializers import ArticleGetSerializer
from Contributions.serializers import Poem_LCU_Serializer
from Posts.serializers import Post_CUD_Serializer
from Articles.models import Article
from Contributions.models import Poem
from Posts.models import Post
from .models import BookMark
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType



class BookMarkSerializer(serializers.ModelSerializer):
    content_data = serializers.SerializerMethodField()
    content_type_name = serializers.SerializerMethodField()

    class Meta:
        model = BookMark
        fields = [
            'id',
            'content_data',
            'content_type_name',
            'added_date',
        ]

    def get_content_data(self, obj):
        request = self.context['request']
        content_object = obj.content_object
        content_type = obj.content_type.model.lower()

        if content_type == "post":
            serializer = Post_CUD_Serializer(content_object, context={'request': request})
        elif content_type == "article":
            serializer = ArticleGetSerializer(content_object, context={'request': request})
        elif content_type == "poem":
            serializer = Poem_LCU_Serializer(content_object, context={'request': request})
        else:
            return None
        return serializer.data
    
    def get_content_type_name(self, obj):
        content_type = obj.content_type.model.lower()
        resource_type_mapping = {
            "article": Article,
            "post": Post,
            "poem": Poem,
        }
        model_class = resource_type_mapping[content_type]

        content_type = ContentType.objects.get_for_model(model_class)
        return content_type.model