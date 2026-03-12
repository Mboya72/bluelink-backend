from django.db import models
from django.conf import settings

class Truck(models.Model):
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='trucks'
    )
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)
    capacity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    current_location = models.CharField(max_length=255)
    
    # ADDED FIELDS:
    description = models.TextField(blank=True, null=True, help_text="Describe truck condition, features, etc.")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.vehicle_number} ({self.vehicle_type})"

# NEW MODEL for multiple pictures:
class TruckImage(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='truck_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.truck.vehicle_number}"


class TransportJob(models.Model):
    class Status(models.TextChoices):
        ASSIGNED = "ASSIGNED", "Assigned"
        PICKED_UP = "PICKED_UP", "Picked Up"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"
        DELIVERED = "DELIVERED", "Delivered"

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transport_jobs",
        null=True,
        blank=True,
    )
    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="delivery",
        null=True,
        blank=True,
    )
    vehicle = models.ForeignKey(
        Truck, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    status = models.CharField(max_length=20, default='PENDING')

    # Current Location
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for Order {self.order.id} - {self.status}"


class GPSLog(models.Model):
    """Stores history for 'Trip Playback' feature."""

    job = models.ForeignKey(
        TransportJob, on_delete=models.CASCADE, related_name="coordinates"
    )
    lat = models.FloatField()
    lng = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class Route(models.Model):
    name = models.CharField(max_length=255, help_text="e.g., Mombasa to Nairobi")
    origin_name = models.CharField(max_length=255)
    origin_lat = models.DecimalField(max_digits=9, decimal_places=6)
    origin_lng = models.DecimalField(max_digits=9, decimal_places=6)
    
    destination_name = models.CharField(max_length=255)
    destination_lat = models.DecimalField(max_digits=9, decimal_places=6)
    destination_lng = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Store the 'road' as a Polyline string (common for Google Maps/Leaflet)
    polyline = models.TextField(help_text="Encoded string representing the road path")
    distance_km = models.DecimalField(max_digits=7, decimal_places=2)
    estimated_time = models.DurationField()

    def __str__(self):
        return self.name

# Link it to your existing TransportJob
class TransportJob(models.Model):
    # ... other fields ...
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)