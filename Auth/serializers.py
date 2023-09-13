from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new User."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    """Serializers registration requests and logs in an existing User."""

    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'refresh': user.tokens['refresh'], 
            'access': user.tokens['access']
        }

class LogoutSerializer(serializers.Serializer):
    """Serializers registration requests and logs out an existing User."""

    refresh = serializers.CharField()

    default_error_message = {
        'invalid_token': ('This Token is either expired or invalid.')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('invalid_token')