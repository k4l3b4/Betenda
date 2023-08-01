from betenda_api.methods import get_reactions_method
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
        fields = [
            'id',
            'language',
            'iso_code',
            'glottolog_code',
            'created_at',
            'edited_at',
            'language_type'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'edited_at': {'read_only': True},
        }

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        fields = [
            'id',
            'translation',
            'word',
            'source_language',
            'target_language',
            'synonym',
            'user',
            'antonym',
            'created_at',
            'edited_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'word': {'required': True, 'validators': [MinLengthValidator(1)]},
            'translation': {'required': True, 'validators': [MinLengthValidator(1)]},
            'user': {'read_only': True},
            'source_language': {'required': True},
            'target_language': {'required': True},
            'created_at': {'read_only': True},
            'edited_at': {'read_only': True},
        }

    def validate(self, data):
        source_language = data.get('source_language')
        target_language = data.get('target_language')

        if source_language and source_language.language_type != 'SOURCE':
            raise serializers.ValidationError(
                {'source_language': 'Invalid source language type.'})

        if target_language and target_language.language_type != 'TARGET':
            raise serializers.ValidationError(
                {'target_language': 'Invalid target language type.'})

        return data

    def create(self, validated_data):
        synonyms = validated_data.pop("synonym", [])
        antonyms = validated_data.pop("antonym", [])
        instance = super().create(validated_data)
        for synonym in synonyms:
            instance.synonym.add(synonym)
        for antonym in antonyms:
            instance.antonym.add(antonym)
        return instance

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class Poem_CUD_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = [
            'id',
            'poem',
            'recording',
            'adult',
            'language',
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

class Poem_Notification_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = [
            'id',
            'poem',
            'slug',
        ]

class SayingSerializer(serializers.ModelSerializer):
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Saying
        fields = [
            'id',
            'saying',
            'language',
            'user',
            'reactions',
            'adult',
            'created_at',
            'edited_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'reactions': {'read_only': True},
            'created_at': {'read_only': True},
            'edited_at': {'read_only': True},
        }

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def get_reactions(self, obj):
        return get_reactions_method(self, obj)


class SentenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sentence
        fields = [
            'id',
            'translation',
            'sentence',
            'user',
            'adult',
            'source_language',
            'target_language',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'word': {'required': True, 'validators': [MinLengthValidator(5)]},
            'translation': {'required': True, 'validators': [MinLengthValidator(5)]},
            'user': {'read_only': True},
            'source_language': {'required': True},
            'target_language': {'required': True},
        }

    def validate(self, data):
        source_language = data.get('source_language')
        target_language = data.get('target_language')

        if source_language and source_language.language_type != 'SOURCE':
            raise serializers.ValidationError(
                {'source_language': 'Invalid source language type.'})

        if target_language and target_language.language_type != 'TARGET':
            raise serializers.ValidationError(
                {'target_language': 'Invalid target language type.'})

        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
