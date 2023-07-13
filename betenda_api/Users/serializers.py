from betenda_api.methods import BadRequest, UnAuthenticated
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator


def validate_terms(value):
    if value != True:
        raise serializers.ValidationError(
            "You have to agree with the terms of service")


class User_CUD_Serializer(serializers.ModelSerializer):
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


class UserTokenSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        print(attrs)
        email = attrs['email']
        password = attrs['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                data = super().validate(attrs)
                refresh = self.get_token(self.user)
                refresh['email'] = self.user.email
                try:
                    data["access"] = str(refresh.access_token)
                    data['lifetime'] = int(
                        refresh.access_token.lifetime.total_seconds())
                except Exception as e:
                    raise BadRequest(e)
                return data
            else:
                raise UnAuthenticated("Account is blocked or not deactivated")
        else:
            raise UnAuthenticated('Incorrect email and password combination!')