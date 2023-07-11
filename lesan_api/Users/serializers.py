from .models import User
from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator

def validate_terms(value):
    if value != True:
        raise serializers.ValidationError("You have to agree with the terms of service")

class UserCreateSerializer(serializers.Serializer):
    user_name = serializers.CharField(validators=[UnicodeUsernameValidator()])
    terms = serializers.BooleanField(validators=[validate_terms])
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_name',
                  'email', 'sex', 'birth_date', 'terms']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': False},
            'user_name': {'required': True},
            'email': {'required': True},
            'sex': {'required': True},
            'birth_date': {'required': True},
            'terms': {'required': True},
        }

    def create(self, validated_data):
        return super().create(validated_data)
