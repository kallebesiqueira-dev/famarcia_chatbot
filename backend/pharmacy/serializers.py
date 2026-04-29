"""Serializer per l'app Pharmacy."""
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer completo per i prodotti farmacia."""
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'available',
            'category', 'category_display', 'requires_prescription',
            'sku', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer leggero per la lista prodotti."""
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'available', 'category', 'requires_prescription']
