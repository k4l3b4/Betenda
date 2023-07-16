from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from betenda_api.methods import BadRequest, UnAuthenticated, send_response
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import FollowerRequest, Invitation, User, UserProfile
from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password


def validate_terms(value):
    if value != True:
        raise serializers.ValidationError(
            "You have to agree with the terms of service")


class User_CUD_Serializer(serializers.ModelSerializer):
    user_name = serializers.CharField(validators=[UnicodeUsernameValidator()])
    terms = serializers.BooleanField(
        validators=[validate_terms], required=True, write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'bio', 'user_name', 'profile_avatar',
                  'email', 'sex', 'birth_date', 'password', 'password2', 'terms', 'verified', 'has_rated', 'is_active', 'joined_date', 'last_login',
                  ]
        extra_kwargs = {
            'id': {'read_only': True},
            'first_name': {'required': True},
            'last_name': {'required': False},
            'user_name': {'required': True},
            'bio': {'read_only': True},
            'profile_avatar': {'read_only': True},
            'email': {'required': True, 'write_only': True},
            'sex': {'required': True},
            'birth_date': {'required': True, 'write_only': True},
            'verified': {'read_only': True},
            'has_rated': {'read_only': True},
            'is_active': {'read_only': True},
            'joined_date': {'read_only': True},
            'last_login': {'read_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise BadRequest("Passwords don't match")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance


# class UserTokenSerializer(TokenObtainPairSerializer):

#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Customize token claims
#         token['email'] = user.email

#         return token

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         user = authenticate(email=email, password=password)
#         if user is not None:
#             if user.is_active:
#                 data = super().validate(attrs)
#                 refresh = RefreshToken.for_user(user)
#                 # Add custom claims to the token
#                 data['access'] = str(refresh.access_token)
#                 data['refresh'] = str(refresh)
#                 data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())

#                 response = Response(data)

#                 # Set cookies in the response
#                 expiration = datetime.now() + refresh.access_token.lifetime
#                 response.set_cookie('access', str(refresh.access_token), httponly=True, secure=True, expires=expiration)
#                 response.set_cookie('refresh', str(refresh), httponly=True, secure=True, expires=timedelta(days=30))

#                 return response
#             else:
#                 raise UnAuthenticated("Account is blocked or not activated")
#         else:
#             raise UnAuthenticated('Incorrect email and password combination!')




class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = [
            'invitation_code',
            'count',
            'disabled',
        ]
        extra_kwargs = {
            'invitation_code': {'read_only': True},
            'count': {'read_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    followed_by_requesting_user = serializers.SerializerMethodField()
    follows_requesting_user = serializers.SerializerMethodField()
    pending_follow_approval = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('user', 'followed_by_requesting_user', 'follows_requesting_user',
                  'pending_follow_approval')

    def get_followed_by_requesting_user(self, obj):
        requesting_user = self.context['request'].user
        return obj.is_followed_by(requesting_user)

    def get_follows_requesting_user(self, obj):
        requesting_user = self.context['request'].user
        return obj.is_following(requesting_user)

    def get_pending_follow_approval(self, obj):
        requesting_user = self.context['request'].user
        requested_user = obj.user
        try:
            exists = FollowerRequest.objects.get(
                user_profile=requested_user.userprofile, follower=requesting_user)
        except:
            return False
        if exists:
            return True


class User_GET_Serializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_name',
                  'bio', 'profile_avatar', 'sex', 'birth_date', 'userprofile']


class FollowerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerRequest
        fields = '__all__'
        depth = 1
