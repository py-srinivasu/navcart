# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.common.responses import APIResponse
from apps.users.models import User
from apps.users.serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(APIView):
    """
    This classbased view will represent the user registration
    this is allowed by any user
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                status='FAILED', code=400,
                message='User creation failed', errors=serializer.errors
            ).json
        user = serializer.save()
        token = Token.objects.create(user=user)
        response = {
            "token": token.key,
            "email": user.email,
            "id": user.id
        }
        return APIResponse(
            status='SUCCESS', code=201,
            message='User Created successfully', extra_fields=response
        ).json


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                status='FAILED', code=400,
                message='User Signin failed, Invalid email/Password', errors=serializer.errors
            ).json

        user = User.objects.get(email=serializer.data.get("email"))
        if not user.check_password(serializer.data["password"]):
            return APIResponse(
                status='FAILED', code=400,
                message='User Signin failed', errors={"error": "Invalid email/Password"}
            ).json

        token, created = Token.objects.get_or_create(user=user)

        response = {
            "token": token.key,
            "email": user.email,
            "id": user.id
        }
        return APIResponse(
            status='SUCCESS', code=200,
            message='User Signed In successfully', extra_fields=response
        ).json
