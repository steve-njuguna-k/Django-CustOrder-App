from .models import Customer
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new Customer."""

    class Meta:
        model = Customer
        fields = '__all__'