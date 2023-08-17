from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from betenda_api.methods import (BadRequest,
                                 check_requested_user_follows,
                                 check_requesting_user_follows, 
                                 check_request_to_be_followed, 
                                 check_request_to_follow)
from .models import FollowerRequest, Invitation, User, UserProfile


def validate_terms(value):
    if value != True:
        raise serializers.ValidationError(
            "You have to agree with the terms of service")


class User_CD_Serializer(serializers.ModelSerializer):
    user_name = serializers.CharField(validators=[UnicodeUsernameValidator()])
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        write_only=True
    )
    followers_count = serializers.IntegerField(
        source='userprofile.followers_count', read_only=True)
    following_count = serializers.IntegerField(
        source='userprofile.following_count', read_only=True)
    request_to_be_followed = serializers.SerializerMethodField()
    request_to_follow = serializers.SerializerMethodField()
    requested_user_follows = serializers.SerializerMethodField()
    requesting_user_follows = serializers.SerializerMethodField()
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
            'password': {'write_only': True},
            'password2': {'write_only': True},
            'profile_cover': {'read_only': True},
            'profile_avatar': {'read_only': True},
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
        return check_request_to_be_followed(self, instance)

    def get_request_to_follow(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        return check_request_to_follow(self, instance)

    def get_requested_user_follows(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        return check_requested_user_follows(self, instance)

    def get_requesting_user_follows(self, instance):
        # Check if the user (instance) follows the requesting user
        return check_requesting_user_follows(self, instance)


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
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    request_to_be_followed = serializers.SerializerMethodField()
    request_to_follow = serializers.SerializerMethodField()
    requested_user_follows = serializers.SerializerMethodField()
    requesting_user_follows = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
                'user', 
                'followers_count',
                'following_count',
                'request_to_be_followed',
                'request_to_follow',
                'requested_user_follows',
                'requesting_user_follows',
                )

    def get_request_to_be_followed(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        return check_request_to_be_followed(self, instance)

    def get_request_to_follow(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        return check_request_to_follow(self, instance)

    def get_requested_user_follows(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        return check_requested_user_follows(self, instance)

    def get_requesting_user_follows(self, instance):
        # Check if the user (instance) follows the requesting user
        return check_requesting_user_follows(self, instance)


class PermissionSerializer(serializers.Serializer):
    codename = serializers.CharField()
    name = serializers.CharField()



class User_GU_Serializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    followers_count = serializers.IntegerField(
        source='userprofile.followers_count', read_only=True)
    following_count = serializers.IntegerField(
        source='userprofile.following_count', read_only=True)
    is_private = serializers.BooleanField(
        source='userprofile.is_private', read_only=True)
    permissions = PermissionSerializer(many=True, read_only=True, source='user_permissions')
    request_to_be_followed = serializers.SerializerMethodField()
    request_to_follow = serializers.SerializerMethodField()
    requested_user_follows = serializers.SerializerMethodField()
    requesting_user_follows = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'bio', 'user_name', 'profile_avatar',
                  'sex',
                  'request_to_be_followed',
                  'request_to_follow',
                  'birth_date',
                  'permissions',
                  'profile_cover',
                  'verified',
                  'followers_count', 'following_count',
                  'is_private',
                  'is_staff',
                  'is_superuser',
                  'requested_user_follows',
                  'requesting_user_follows',
                  'has_rated', 'is_active', 'joined_date', 'last_login',
                  ]
        extra_kwargs = {
            'verified':{'read_only':True},
            'has_rated':{'read_only':True},
            'is_active':{'read_only':True},
            'joined_date':{'read_only':True},
            'last_login':{'read_only':True},
        }

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def get_request_to_be_followed(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        return check_request_to_be_followed(self, instance)

    def get_request_to_follow(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        return check_request_to_follow(self, instance)

    def get_requested_user_follows(self, instance):
        # Check if the requesting user (if authenticated) follows the user
        return check_requested_user_follows(self, instance)

    def get_requesting_user_follows(self, instance):
        # Check if the user (instance) follows the requesting user
        return check_requesting_user_follows(self, instance)





class FollowerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerRequest
        fields = '__all__'


class User_SIMPLE_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'profile_avatar', 'user_name', 'first_name', 'last_name']
