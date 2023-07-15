from rest_framework import generics, mixins
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from Users.models import FollowerRequest, Invitation, UserProfile
from Users.serializers import User_CUD_Serializer, UserProfileSerializer, UserTokenSerializer
from betenda_api.methods import BadRequest, PermissionDenied, UselessRequest, save_notification, send_notification, send_response
from rest_framework.permissions import AllowAny

# Create your views here.


class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = User_CUD_Serializer

    def post(self, request, code, format=None):
        try:
            invite = Invitation.objects.get(
                invitation_code=code, disabled=False, expired=False)
        except:
            raise PermissionDenied(
                "You are not authorized to register an account")

        # Just in case the invitation instance wasn't deleted for some reason

        if invite.count < 10:
            serializer = User_CUD_Serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(invited_by=invite.user)
                invite.count = invite.count + 1
                invite.save()
                return send_response(serializer.data, "Account registered successfully")
            raise BadRequest(serializer.errors)
        invite.expired = True
        invite.save()
        raise PermissionDenied(
            "Opps.. the invitation code has expired, guess someone beat you to it.")


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny,]
    serializer_class = UserTokenSerializer

    # def post(self, request):
    #     serializer = UserTokenSerializer(data=request.data)
    #     if serializer.is_valid():
    #         validated_data = serializer.validate(serializer.validated_data)
    #         return send_response(validated_data, 'Authentication successful')
    #     raise BadRequest(serializer.errors)

    # # Get the user's device information
    # device, created = Device.objects.get_or_create(
    #     user=serializer.user,
    #     defaults={
    #         'ip_address': request.META.get('REMOTE_ADDR', None),
    #         'device_type': request.META.get('HTTP_USER_AGENT', None),
    #         'device_name': f"{request.user_agent.device.family} - {request.user_agent.os.family}({request.user_agent.os.version_string})",
    #         'browser_type': request.user_agent.browser.family,
    #         'browser_version': request.user_agent.browser.version_string,
    #         'operating_system': f"{request.user_agent.os.family} - {request.user_agent.os.version_string}",
    #         'logged_in': False,
    #     }
    # )

    # if not device.logged_in:
    #     return send_response(None, 'We have just sent you an email, authenticate your self', 200)


class UserProfileFollowAPIView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        '''
        follow the user that was requested
        '''
        user_profile = self.get_object()
        user = request.user
        if user_profile.user_id == user.id:
            # Raise an exception if the user is trying to follow them selves
            # NOTE: there should be no way to do this in the frontend but there is no such thing as being to secure so...
            raise UselessRequest("Trying to follow your self isn't allowed😂")

        if not user_profile.is_private:
            # If the user profile is not private, add the follower directly
            user_profile.followers.add(user)
            user_profile.followers_count += 1
            user_profile.save()
            notification = save_notification(
                user=user_profile, message=f"@{user.user_name} has started following you!")
            send_notification(user_profile.user_id, notification)
            return send_response('You are now following this user.')

        # If the user profile is private, create a follower request
        follower_request, created = FollowerRequest.objects.get_or_create(
            user_profile=user_profile,
            follower=user
        )

        if created:
            notification = save_notification(
                user=user_profile, message=f"@{user.user_name} has requested to follow you!")
            send_notification(user_profile.user_id, notification)
            return send_response('Your request to follow this user has been sent.')
        else:
            follower_request.delete()
            # abstracted method to send a Response object
            return send_response('Your follow request has been canceled')

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_profile = self.get_object()
        user_profile.followers.remove(request.user)
        user_profile.followers_count -= 1
        user_profile.save()
        return send_response('Your follow request has been canceled')
