# 708115538
from random import choices

from rest_framework.fields import MinLengthValidator
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
            'translation',
            'word',
            'source_language',
            'target_language',
            'synonym',
            'antonym',
        ]
        extra_kwargs = {
            'word': {'required': True, 'validators': [MinLengthValidator(1)]},
            'translation': {'required': True, 'validators': [MinLengthValidator(1)]},
            'source_language': {'required': True},
            'target_language': {'required': True},
        }
        
    def validate(self, data):
        source_language = data.get('source_language')
        target_language = data.get('target_language')

        if source_language and source_language.language_type != 'SOURCE':
            raise serializers.ValidationError({'source_language': 'Invalid source language type.'})

        if target_language and target_language.language_type != 'TARGET':
            raise serializers.ValidationError({'target_language': 'Invalid target language type.'})

        return data
    
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
            'translation',
            'sentence',
            'source_language',
            'target_language',
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
