
from django.http import JsonResponse
from rest_framework import status

# Create your views here.
def oauth_openid_callback(request):
    code = request.GET['code']
    params = {
        "code": code
    }
    return JsonResponse({"status":status.HTTP_200_OK, "message": "Authorization Code Generated Successfully!", "results": params})