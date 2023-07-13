from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from Users.models import Device, Invitation
from Users.serializers import User_CUD_Serializer, UserTokenSerializer
from betenda_api.methods import BadRequest, PermissionDenied, send_response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# Create your views here.


class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = User_CUD_Serializer

    def post(self, request, code, format=None):
        try:
            invite = Invitation.objects.get(invitation_code=code)
        except:
            raise PermissionDenied("You are not authorized to register an account")

        serializer = User_CUD_Serializer(request.data)

        # Just in case the invitation instance wasn't deleted for some reason
        if invite.count < 11:
            if serializer.is_valid():
                serializer.save()
                return send_response(serializer.data, "Account registered successfully")
            raise BadRequest(serializer.errors)
        raise PermissionDenied("You are not authorized to register for an account")


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