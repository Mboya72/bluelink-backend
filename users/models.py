from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email: 
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN') # Default superusers to ADMIN role

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Removed username for email-only login
    email = models.EmailField(unique=True)
    
    class Role(models.TextChoices):
        USER = 'USER', 'Regular User' # Added this so the default works
        FISHERMAN = 'FISHERMAN', 'Fisherman'
        BUYER = 'BUYER', 'Buyer'
        SELLER = 'SELLER', 'Seller'
        DRIVER = 'DRIVER', 'Driver'
        STORAGE = 'STORAGE', 'Storage'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.USER # Using the class reference is safer
    )
    
    is_verified_seller = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # No username means this stays empty

    objects = UserManager()

    def __str__(self):
        return self.email

# --- Profile Models ---

class FishermanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fisherman_profile')
    license_number = models.CharField(max_length=50)
    boat_details = models.TextField()
    landing_site = models.CharField(max_length=255)

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    vehicle_reg = models.CharField(max_length=20)
    capacity_kg = models.PositiveIntegerField()