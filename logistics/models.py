from django.db import models
from django.conf import settings


class Vehicle(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(
        max_length=50
    )  # e.g., Lorry, Motorbike, Freezer Truck
    capacity_kg = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.plate_number} ({self.vehicle_type})"


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
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ASSIGNED
    )

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
