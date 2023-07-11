# 708115538
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Poem, Saying, Sentence, Word, Language


class LanguageSerializer(serializers.ModelSerializer):
    language = serializers.CharField(
        validators=[UniqueValidator(queryset=Language.objects.all())])
    glottolog_code = serializers.CharField(
        validators=[UniqueValidator(queryset=Language.objects.all())])

    class Meta:
        model = Language
        fields = ['language', 'iso_code', 'glottolog_code', 'language_type']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'word',
            'source_language',
            'target_language',
            'synonym',
            'antonym',
        ]
        extra_kwargs = {
            'word': {'required': True},
        }

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PoemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = [
            'poem',
            'language',
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class SayingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saying
        fields = [
            'saying',
            'language',
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = [
            'sentence',
            'source_language',
            'target_language',
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
