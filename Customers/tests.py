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
from .models import Customer

Application = get_application_model()

class CustomerTestCase(TestCase):
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
        self.access_token = token_info.get("access_token")
        self.assertIsNotNone(self.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
    
    def test_create_customer(self):
        # Define the data for the new customer
        data = {
            'first_name': 'Steve',
            'last_name': 'Harvey',
            'phone_number': '0712345678',
        }

        # Send a POST request to create a new customer
        response = self.client.post(f'/api/v1/customers', data)
        response_info = json.loads(response.content)

        # Check if the request was successful (HTTP status code 201 - Created)
        self.assertEqual(response_info['status'], 201)

        # Check if the customer was created in the database
        self.assertTrue(Customer.objects.filter(first_name='Steve').exists())

    def test_read_customer(self):
        # Create a test customer
        customer = Customer.objects.create(
            first_name='Jesicca',
            last_name='Pearson',
            phone_number='0711223344'
        )

        # Send a GET request to retrieve the customer details
        response = self.client.get(f'/api/v1/customers/{customer.id}')
        response_info = json.loads(response.content)

        # Check if the request was successful (HTTP status code 200 - OK)
        self.assertEqual(response_info['status'], 200)

        # Check if the returned data matches the created customer
        self.assertEqual(response_info['results']['first_name'], 'Jesicca')
        self.assertEqual(response_info['results']['last_name'], 'Pearson')
        self.assertEqual(response_info['results']['phone_number'], '0711223344')

    def test_update_customer(self):
        # Create a test customer
        customer = Customer.objects.create(
            first_name='Mike',
            last_name='Ross',
            phone_number='0798765432'
        )

        # Define the updated data for the customer
        updated_data = {
            'first_name': 'Louis',
            'last_name': 'Litt',
            'phone_number': '0722333444',
        }

        # Send a PUT request to update the customer details
        response = self.client.patch(f'/api/v1/customers/{customer.id}', updated_data, format='json')
        response_info = json.loads(response.content)

        # Check if the request was successful (HTTP status code 200 - OK)
        self.assertEqual(response_info['status'], 200)

        # Check if the customer details were updated in the database
        customer.refresh_from_db()
        self.assertEqual(customer.first_name, 'Louis')
        self.assertEqual(customer.last_name, 'Litt')
        self.assertEqual(customer.phone_number, '0722333444')

    def test_delete_customer(self):
        # Create a test customer
        customer = Customer.objects.create(
            first_name='Steve',
            last_name='Harvey',
            phone_number='0712345678'
        )

        # Send a DELETE request to delete the customer
        response = self.client.delete(f'/api/v1/customers/{customer.id}')
        response_info = json.loads(response.content)

        # Check if the request was successful (HTTP status code 204 - No Content)
        self.assertEqual(response_info['status'], 204)

        # Check if the customer was deleted from the database
        self.assertFalse(Customer.objects.filter(id=customer.id).exists())