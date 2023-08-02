from random import sample
from django.contrib.auth import login
from django.db.models import F, Q
from django.middleware import csrf
from rest_framework import generics, viewsets
from rest_framework.authentication import authenticate
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from Users.models import FollowerRequest, Invitation, User, UserProfile
from Users.serializers import User_SIMPLE_Serializer
from Users.serializers import (FollowerRequestSerializer, LoginSerializer,
                               User_CUD_Serializer, User_GET_Serializer,
                               UserProfileSerializer)
from betenda_api.methods import (BadRequest, PermissionDenied,
                                 ResourceNotFound, ServerError,
                                 UnAuthenticated, UselessRequest,
                                 save_notification, send_notification,
                                 send_response, validate_key_value, send_error, ErrorType)

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
            "Oops.. the invitation code has expired, guess someone beat you to it.")


# class LoginView(TokenObtainPairView):
#     permission_classes = [AllowAny,]
#     serializer_class = UserTokenSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'lifetime': str(refresh.access_token.lifetime.total_seconds()),
    }


class LoginView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = LoginSerializer  # for the api browser fields

    def post(self, request, format=None):
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            print(user)
            if user.is_active:
                login(request, user)
                data = get_tokens_for_user(user)
                return send_response(data, 'Login successful')
            return send_error(ErrorType.UNAUTHORIZED, "Account is blocked or not activated", 403)
        raise UnAuthenticated('Incorrect email and password combination!')


class AuthorSearchView(generics.ListAPIView):
    serializer_class = User_SIMPLE_Serializer

    def get_queryset(self):
        queryset = User.objects.all()
        # If 'search' query parameter is provided, perform search filtering
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(Q(user_name__icontains=search_term) | Q(first_name__icontains=search_term)| Q(last_name__icontains=search_term) | Q(id__iexact=search_term))
        # Filter staff or superuser users
        queryset = queryset.filter(Q(is_staff=True) | Q(is_superuser=True))
        return queryset[:20]
    
class CurrentUserView(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = User_CUD_Serializer

    @action(detail=True, methods=['get'])
    def get_current_user(self, request):
        """
        Returns the current user
        """
        user_instance = self.queryset.filter(
            pk=request.user.id).select_related('userprofile').first()
        # user_instance = self.get_object().select_related('userprofile')
        serializer = self.serializer_class(
            user_instance, context={'request': request})
        return send_response(serializer.data, "Self retrieved successfully")


    @action(detail=True, methods=['patch'])
    def update_current_user(self, request):
        """
        Returns the current user
        """
        user = request.user
        data = request.data
        serializer = User_GET_Serializer(instance=user, data=data, partial=True)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save()
        return send_response(None, "Profile updated successfully")

    @action(detail=True, methods=['get'])
    def get_followers(self, request, *args, **kwargs):
        user = request.user
        # Get the users who are following the requested user
        users_following_requested_user = User.objects.filter(
            userprofile__following=user
        ).exclude(id=user.id)[:20]

        # Combine the two querysets
        serializer = self.serializer_class(users_following_requested_user, many=True, context={'request': request})
        return send_response(serializer.data, f"List retrieved successfully")

    @action(detail=True, methods=['get'])
    def get_user(self, request, *args, **kwargs):
        username = request.GET.get('username')
        # Raises an exception if the key isn't present or is an empty string
        validate_key_value(username, "username")
        user = self.queryset.filter(
            user_name=username).select_related('userprofile').first()
        if user:
            serializer = self.serializer_class(user, context={'request': request})
            return send_response(serializer.data, f"{user.first_name} retrieved successfully")
        raise ResourceNotFound("User not found")
    
    @action(detail=False, methods=['get'])
    def mutual_friends_following(self, request):
        current_user_profile = request.user.user_profile
        current_user_friends = current_user_profile.get_friends()

        friends_following = User.objects.filter(user_profile__followers=request.user)

        mutual_friends_following = friends_following.filter(user_profile__following__in=current_user_friends).distinct()

        serializer = User_GET_Serializer(mutual_friends_following, many=True)
        return Response(serializer.data)



class UserProfileFollowAPIView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        '''
        follow the user that was requested
        '''
        try:
            user_profile = self.queryset.get(user_id=pk)
        except:
            raise ResourceNotFound("User was not found")
        
        user = request.user
        if user_profile.user_id == user.id:
            # Raise an exception if the user is trying to follow them selves
            # NOTE: there should be no way to do this in the frontend but there is no such thing as being to secure so...
            raise UselessRequest("Trying to follow your self isn't allowed😂")
        already_following = None
        try:
            already_following = user_profile.followers.get(id=user.id)
        except:
            pass

        if already_following:
            raise UselessRequest(
                f'You are already following {user_profile.user.first_name}!')

        if not user_profile.is_private:
            # If the user profile is not private, add the follower directly
            user_profile.followers.add(user)
            user_profile.followers_count += 1
            user_profile.save()

            # Update request.user's follower's following count
            user.userprofile.following.add(user_profile.user)
            user.userprofile.following_count += 1
            user.userprofile.save()

            notification = save_notification(
                user=user_profile.user, sender=request.user, type="2", message="Has started following you!")
            send_notification(user_profile.user_id, notification)
            return send_response(None, f'You are now following {user_profile.user.first_name}!')

        # If the user profile is private, create a follower request
        follower_request, created = FollowerRequest.objects.get_or_create(
            user_profile=user_profile,
            follower=user,
            is_approved=False
        )

        if created:
            notification = save_notification(
                user=user_profile.user, sender=request.user, type="2", message="Has requested to following you!")
            send_notification(user_profile.user_id, notification)
            return send_response(None, 'Your request to follow this user has been sent.')
        else:
            follower_request.delete()
            # abstracted method to send a Response object
            return send_response(None, 'Your follow request has been canceled')

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user = request.user
        try:
            user_profile = self.queryset.get(user_id=pk)
        except:
            raise ResourceNotFound("User Profile was not found")
        if user_profile.user_id == user.id:
            # Raise an exception if the user is trying to unfollow them selves
            # NOTE: there should be no way to do this in the frontend but there is no such thing as being to secure so...
            raise UselessRequest("Trying to unfollow your self isn't allowed😂")

        followers = user_profile.followers.all()
        if not followers.filter(pk=user.pk).exists():
            raise ResourceNotFound("You are not following this user")

        if user_profile.followers_count > 0:
            user_profile.followers_count = F('followers_count') - 1
            user_profile.save(update_fields=['followers_count'])

        user_profile.followers.remove(user)

        if user.userprofile.following_count > 0:
            user.userprofile.following_count = F('following_count') - 1
            user.userprofile.save(update_fields=['following_count'])

        user.userprofile.following.remove(user_profile.user)

        return send_response(None, f'You have unfollowed {user_profile.user.first_name}')

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        user = request.user
        try:
            user_profile = self.queryset.get(user=user)
        except:
            raise ResourceNotFound("User was not found")
        try:
            follow_request = FollowerRequest.objects.get(
                user_profile=user_profile, follower_id=pk, is_approved=False)
        except:
            raise ResourceNotFound("Request was not found")
        try:
            follow_request.follower.userprofile.following_count += 1
            follow_request.follower.userprofile.save()

            follow_request.follower.userprofile.following.add(user)

            user.userprofile.followers_count += 1
            user.userprofile.save()

            user.userprofile.followers.add(follow_request.follower)

            notification = save_notification(
                user=follow_request.follower, type="2", message="Has accepted your follow request!")
            send_notification(
                follow_request.follower_id, notification)

            follow_request.is_approved = True
            follow_request.save()
            return send_response(None, f"You have accepted {follow_request.follower.first_name}'s request to follow you!")
        except:
            raise ServerError(
                "An error occurred on our side.")


class User_GET_View(generics.RetrieveAPIView):
    serializer_class = User_GET_Serializer
    queryset = User.objects.filter(is_active=True)

    def get(self, request, username, *args, **kwargs):
        try:
            user = self.queryset.get(user_name=username)
        except:
            raise ResourceNotFound("User was not found")
        serializer = User_GET_Serializer(user, context={'request': request})
        return send_response(serializer.data, "User retrieved successfully")


class FollowerRequestListView(generics.ListAPIView):
    serializer_class = FollowerRequestSerializer

    def get(self):
        user = self.request.user
        data = FollowerRequest.objects.filter(user_profile__user=user)
        serializer = self.serializer_class(data)
        return send_response(serializer.data, "All follow requests")
