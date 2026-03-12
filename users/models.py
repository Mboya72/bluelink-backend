from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email: raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Using email for login instead of username
    email = models.EmailField(unique=True)
    
    class Role(models.TextChoices):
        FISHERMAN = 'FISHERMAN', 'Fisherman'
        BUYER = 'BUYER', 'Buyer'
        SELLER = 'SELLER', 'Seller'
        DRIVER = 'DRIVER', 'Driver'
        STORAGE = 'STORAGE', 'Storage'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.BUYER)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

# Example of a Type-Specific Profile
class FishermanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fisherman_profile')
    license_number = models.CharField(max_length=50)
    boat_details = models.TextField()
    landing_site = models.CharField(max_length=255)

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    vehicle_reg = models.CharField(max_length=20)
    capacity_kg = models.PositiveIntegerField()