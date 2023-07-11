from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from Users.models import Device, Invitation, User
from Users.serializers import UserCreateSerializer
from lesan_api.methods import BadRequest, PermissionDenied, send_response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# Create your views here.


class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request, code, format=None):
        try:
            invite = Invitation.objects.get(invitation_code=code)
        except:
            raise PermissionDenied("You are not authorized to register an account")

        serializer = UserCreateSerializer(request.data)

        # Just in case the invitation instance wasn't deleted for some reason
        if invite.count < 11:
            if serializer.is_valid():
                serializer.save()
                return send_response(serializer.data, "Account registered successfully")
            raise BadRequest(serializer.errors)
        raise PermissionDenied("You are not authorized to register for an account")


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)

        # Get the user's device information
        device_id = request.device.device_id
        device, created = Device.objects.get_or_create(
            user=serializer.user,
            device_id=device_id,
            defaults={
                'ip_address': request.META.get('REMOTE_ADDR', None),
                'device_type': request.META.get('HTTP_USER_AGENT', None),
                'device_name': request.device.device_name,
                'city': request.device.city,
                'country': request.device.country,
                'operating_system': request.device.operating_system,
                'logged_in': False,
            }
        )

        if not device.logged_in:
            return send_response(None, 'We have just sent you an email, authenticate your self', 200)

        # The device exists, proceed with authentication and token generation
        refresh = RefreshToken.for_user(serializer.user)
        access = refresh.access_token
        lifetime = refresh.access_token.lifetime.total_days()
        data = {
            'refresh': str(refresh),
            'access': str(access),
            'lifetime': int(lifetime),
        }
        return send_response(data, 'Authentication successful', 200)
