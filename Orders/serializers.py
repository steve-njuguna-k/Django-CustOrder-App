from .models import Order
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new Order."""

    class Meta:
        model = Order
        fields = '__all__'