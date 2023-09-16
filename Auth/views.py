
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import (LoginSerializer, RegistrationSerializer)
from rest_framework import status

# Create your views here.
def oauth_openid_callback(request):
    code = request.GET['code']
    params = {
        "code": code
    }
    return JsonResponse({"status":status.HTTP_200_OK, "message": "Authorization Code Generated Successfully!", "results": params})

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
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                return JsonResponse({"status":status.HTTP_200_OK, "message": "Log In Successful!"})
            else:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})
        
class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Return user after login."""
        try:
            request.data.auth_token.delete()
            return JsonResponse({"status":status.HTTP_204_NO_CONTENT, "message": "You have logged out!",})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})