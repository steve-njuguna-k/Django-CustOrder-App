import json
from urllib.parse import parse_qs, urlparse
from django.test import TestCase
from django.urls import reverse
from oauth2_provider.models import get_application_model
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import random
import string
import base64
import hashlib
import secrets

Application = get_application_model()

class OAuth2AuthorizationCodeFlowTestCase(TestCase):
    def setUp(self):
        # Set up test OAuth2 client credentials and other required data
        self.client_id = secrets.token_urlsafe(16)
        self.client_secret = secrets.token_urlsafe(50)
        
        # Create a test OAuth2 application
        self.application = Application.objects.create(
            name="Test Application",
            client_id=self.client_id,
            client_secret=self.client_secret,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris="http://localhost:8000/o/callback",
            algorithm=Application.RS256_ALGORITHM
        )

        # Set up data for creating a superuser
        self.superuser_data = {
            'username': 'admin',
            'password': 'adminpassword',
            'email': 'admin@example.com',
        }

        # Generate code verifier and challenge for PKCE (Proof Key for Code Exchange)
        code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
        code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))
        self.verifier = code_verifier.decode('utf-8')

        code_challenge = hashlib.sha256(code_verifier).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
        self.challenge = code_challenge

        # Create a superuser for testing
        self.user = User.objects.create_superuser(username=self.superuser_data["username"], email=self.superuser_data['email'], password=self.superuser_data["password"])
        self.client = APIClient(raise_request_exception=True)

    def test_superuser_created(self):
        # Check if the superuser has been created successfully
        superuser = User.objects.filter(username=self.superuser_data['username'], is_superuser=True).first()
        self.assertIsNotNone(superuser)

    def test_user_login(self):
        # Test user login functionality
        response = self.client.login(username=self.superuser_data['username'], password=self.superuser_data['password'])
        self.assertEqual(response, True)

    def test_create_oauth_application(self):
        # Test creating an OAuth application
        self.client.login(username=self.superuser_data['username'], password=self.superuser_data['password'])

        application_data = {
            'name': 'Test Application',
            'client_id': secrets.token_urlsafe(16),
            'client_secret': secrets.token_urlsafe(50),
            'client_type': 'confidential',
            'authorization_grant_type': 'authorization-code',
            'redirect_uris': 'http://localhost:8000/o/callback'
        }

        response = self.client.post(reverse('oauth2_provider:register'), application_data)
        self.assertEqual(response.status_code, 302)

        application = Application.objects.filter(name=application_data['name']).first()
        self.assertIsNotNone(application)

    def test_authorization_code_flow(self):
        # Test the OAuth2 authorization code flow
        self.client.login(username=self.superuser_data['username'], password=self.superuser_data['password'])

        authorization_url = reverse("oauth2_provider:authorize")
        response = self.client.get(
            authorization_url, {
                "response_type": "code",
                "code_challenge": self.challenge,
                "code_challenge_method": "S256",
                "client_id": self.application.client_id,
                "redirect_uri": self.application.redirect_uris.split()[0],
                "scope": "openid"
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('oauth2_provider:authorize'), {
            "response_type": "code",
            "code_challenge": self.challenge,
            "code_challenge_method": "S256",
            "client_id": self.application.client_id,
            "redirect_uri": self.application.redirect_uris.split()[0],
            "scope": "openid",
            'allow': True
        })
        self.assertEqual(response.status_code, 302)

        redirect_url = response.url
        parsed_url = urlparse(redirect_url)
        query_parameters = parse_qs(parsed_url.query)
        authorization_code = query_parameters.get('code', [])

        # simulate the callback url response status code
        callback_url = reverse('oauth_open_id_callback')
        response = self.client.get(callback_url, {
            'code': authorization_code[0],
            'state': secrets.token_urlsafe(50),
        })
        self.assertEqual(response.status_code, 200)

        # Request an access token using the authorization code
        token_data = {
            "grant_type": "authorization_code",
            "code": authorization_code[0],
            "redirect_uri": self.application.redirect_uris.split()[0],
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code_verifier": self.verifier
        }
    
        token_url = reverse("oauth2_provider:token")
        response = self.client.post(token_url, token_data)

        self.assertEqual(response.status_code, 200)

        # Check if an access token is obtained successfully and use it to make a resource request
        token_info = json.loads(response.content)
        access_token = token_info.get("access_token")
        self.assertIsNotNone(access_token)

        resource_url = reverse("list_create_orders")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(resource_url)
        self.assertEqual(response.status_code, 200)