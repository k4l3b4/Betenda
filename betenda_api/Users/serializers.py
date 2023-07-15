from betenda_api.methods import BadRequest, UnAuthenticated
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import FollowerRequest, Invitation, User, UserProfile
from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator


def validate_terms(value):
    if value != True:
        raise serializers.ValidationError(
            "You have to agree with the terms of service")


class User_CUD_Serializer(serializers.ModelSerializer):
    user_name = serializers.CharField(validators=[UnicodeUsernameValidator()])
    terms = serializers.BooleanField(
        validators=[validate_terms], required=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'bio', 'user_name', 'profile_avatar',
                  'email', 'sex', 'birth_date', 'password', 'terms']
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
            'password': {'required': True, 'write_only': True},
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
                raise UnAuthenticated("Account is blocked or not activated")
        else:
            raise UnAuthenticated('Incorrect email and password combination!')


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
    follows_requesting_user = serializers.SerializerMethodField()
    follows_requesting_user = serializers.SerializerMethodField()
    pending_follow_approval = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('follows_requesting_user', 'follows_requesting_user',
                  'pending_follow_approval')

    def get_follows_requesting_user(self, obj):
        requesting_user = self.context['request'].user
        return obj.is_followed_by(requesting_user)

    def get_follows_requesting_user(self, obj):
        requesting_user = self.context['request'].user
        return obj.is_following(requesting_user)

    def get_pending_follow_approval(self, obj):
        requesting_user = self.context['request'].user
        requested_user = obj.user
        return FollowerRequest.objects.filter(user_profile=requested_user.user_profile, follower=requesting_user).exists()


class FollowerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerRequest
        fields = '__all__'
