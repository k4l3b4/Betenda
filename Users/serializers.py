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
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    followers_count = serializers.IntegerField(
        source='userprofile.followers_count', read_only=True)
    following_count = serializers.IntegerField(
        source='userprofile.following_count', read_only=True)
    request_to_be_followed = serializers.SerializerMethodField(read_only=True)
    request_to_follow = serializers.SerializerMethodField(read_only=True)
    requested_user_follows = serializers.SerializerMethodField(read_only=True)
    requesting_user_follows = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'bio', 'user_name', 'profile_avatar',
                  'email', 'sex',
                  'request_to_be_followed',
                  'request_to_follow',
                  'birth_date',
                  'profile_cover',
                  'password', 'password2',
                  'verified',
                  'followers_count', 'following_count',
                  'requested_user_follows',
                  'requesting_user_follows',
                  'has_rated', 'is_active', 'joined_date', 'last_login',
                  ]

        extra_kwargs = {
            'id': {'read_only': True},
            'first_name': {'required': True},
            'last_name': {'required': False},
            'user_name': {'required': True},
            'bio': {'read_only': True},
            'profile_cover': {'read_only': True},
            'profile_avatar': {'read_only': True},
            'email': {'required': True, 'write_only': True},
            'sex': {'required': False},
            'birth_date': {'required': False, 'write_only': True},
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

    def get_request_to_be_followed(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        requesting_user = self.context['request'].user
        # if the user is requesting his own account return None
        if instance != requesting_user:
            try:
                exists = FollowerRequest.objects.get(
                    user_profile=requesting_user.userprofile,
                    follower=instance,
                    is_approved=False
                )

            except:
                return False
            if exists:
                return True
        return None

    def get_request_to_follow(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        try:
          requesting_user = self.context['request'].user
        except:
          return False
        # if the user is requesting his own account return None
        if instance != requesting_user:
            try:
                exists = FollowerRequest.objects.get(
                    user_profile=instance.userprofile,
                    follower=requesting_user,
                    is_approved=False
                )
            except:
                return False

            if exists:
                return True
        return None

    def get_requested_user_follows(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        try:
          requesting_user = self.context['request'].user
        except:
          return False
        # if the user is requesting his own account return None
        if instance != requesting_user:
            try:
                exists = instance.userprofile.following.get(
                    pk=requesting_user.pk)
            except:
                return False

            if exists:
                return True
        return None

    def get_requesting_user_follows(self, instance):
        # Check if the user (instance) follows the requesting user
        try:
          requesting_user = self.context['request'].user
        except:
          return False
        # if the user is requesting his own account return None
        if instance != requesting_user:
            try:
                exists = instance.userprofile.followers.get(
                    pk=requesting_user.pk)
            except:
                return False
            if exists:
                return True
        return None


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password']


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
        fields = ['id', 'first_name', 'last_name', 'user_name', 'email',
                  'bio', 'profile_avatar', 'profile_cover', 'sex', 'birth_date', 'userprofile']

        extra_kwargs = {
            'id': {'read_only': True},
            'userprofile': {'read_only': True},
            'email': {'write_only': True},
        }


class FollowerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerRequest
        fields = '__all__'


class User_SIMPLE_Serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'user_name']
