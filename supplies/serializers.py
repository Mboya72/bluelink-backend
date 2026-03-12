from rest_framework import serializers
from .models import Supply

class SupplySerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.username')
    # Use ImageField to ensure the full URL (including http://...) is returned
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Supply
        fields = [
            'id', 
            'vendor', 
            'vendor_name', 
            'item_name', 
            'brand', 
            'description', 
            'image',      # <--- Added image field here
            'price', 
            'stock_count', 
            'is_available',
            'created_at'   # Good to include for the seller's history
        ]
        read_only_fields = ['vendor']