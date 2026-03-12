from django.db import models
from django.conf import settings

class Supply(models.Model):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    
    # Corrected ImageField
    # 'upload_to' creates a folder in your media storage
    image = models.ImageField(upload_to='supplies_images/', null=True, blank=True)
    
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock_count = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} - {self.brand}"