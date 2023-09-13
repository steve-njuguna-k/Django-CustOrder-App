
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import (LoginSerializer, RegistrationSerializer, LogoutSerializer)
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework import status

# Create your views here.
class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request: Request) -> JsonResponse:
        """Return user response after a successful registration."""
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({"status":status.HTTP_201_CREATED, "message": "Registration Successful! You can proceed to Log In", "results": serializer.data})
            else:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})
        
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request: Request) -> JsonResponse:
        """Return user after login."""
        try:
            user = request.data.get('user', {})

            serializer = self.serializer_class(data=user)
            if serializer.is_valid():
                return JsonResponse({"status":status.HTTP_200_OK, "message": "Log In Successful!", "results": serializer.data})
            else:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})
        
class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Return user after login."""
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            LogoutAllView.as_view()(request=request._request)
            return JsonResponse({"status":status.HTTP_204_NO_CONTENT, "message": "You have logged out!",})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})
        
class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Logs you out of all systems a user had logged in"""
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return JsonResponse({"status":status.HTTP_205_RESET_CONTENT, "message": "Logged Out From All Devices Successfully!"})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})