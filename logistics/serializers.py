from rest_framework import serializers
from .models import Truck, TruckImage, TransportJob, Route

class TruckImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckImage
        fields = ['id', 'image', 'uploaded_at']

class TruckSerializer(serializers.ModelSerializer):
    images = TruckImageSerializer(many=True, read_only=True)
    # This allows you to send new files in a PATCH request
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Truck
        fields = [
            'id', 'driver', 'vehicle_number', 'vehicle_type', 
            'capacity_kg', 'current_location', 'description', 
            'is_available', 'images', 'uploaded_images'
        ]
        read_only_fields = ['driver']

    def update(self, instance, validated_data):
        # 1. Handle new images if provided in the PATCH
        uploaded_images = validated_data.pop('uploaded_images', None)
        if uploaded_images:
            for image in uploaded_images:
                TruckImage.objects.create(truck=instance, image=image)
        
        # 2. Update all other fields (including description)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        # Remove images from data before creating the Truck instance
        uploaded_images = validated_data.pop('uploaded_images', [])
        truck = Truck.objects.create(**validated_data)
        
        # Create image instances for each uploaded file
        for image in uploaded_images:
            TruckImage.objects.create(truck=truck, image=image)
        return truck

# Also add the one your view was looking for to stop the error
class TransportJobSerializer(serializers.ModelSerializer):
    class Meta:
        # If you don't have a TransportJob model yet, 
        # just comment out the import in views.py instead
        fields = '__all__'
        
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class TransportJobSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True) # Nested route details
    
    class Meta:
        model = TransportJob
        fields = ['id', 'vehicle', 'status', 'route', 'current_lat', 'current_lng']