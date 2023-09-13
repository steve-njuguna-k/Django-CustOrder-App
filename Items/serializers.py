from .models import Item
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new Item."""

    class Meta:
        model = Item
        fields = '__all__'