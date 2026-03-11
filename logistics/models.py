from django.db import models
from users.models import User

class Vehicle(models.Model):

    driver = models.ForeignKey(User, on_delete=models.CASCADE)

    vehicle_type = models.CharField(max_length=100)

    plate_number = models.CharField(max_length=50)

    capacity_kg = models.FloatField()

    photo = models.ImageField(upload_to="vehicles/")

    available = models.BooleanField(default=True)


class TransportBooking(models.Model):

    fisherman = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fisherman")

    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="driver")

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    pickup_location = models.CharField(max_length=255)

    destination = models.CharField(max_length=255)

    status = models.CharField(max_length=50, choices=[
        ("requested", "Requested"),
        ("accepted", "Accepted"),
        ("in_transit", "In Transit"),
        ("delivered", "Delivered")
    ])

    created_at = models.DateTimeField(auto_now_add=True)