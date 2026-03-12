from rest_framework import serializers
from .models import Truck # Make sure your model is named Truck

class TruckSerializer(serializers.ModelSerializer):
    driver_name = serializers.ReadOnlyField(source='driver.username')

    class Meta:
        model = Truck
        fields = ['id', 'driver_name', 'vehicle_number', 'vehicle_type', 'capacity_kg', 'current_location', 'is_available']
        read_only_fields = ['driver']

# Also add the one your view was looking for to stop the error
class TransportJobSerializer(serializers.ModelSerializer):
    class Meta:
        # If you don't have a TransportJob model yet, 
        # just comment out the import in views.py instead
        fields = '__all__'