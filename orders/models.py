from django.db import models
from django.conf import settings


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid (Escrow)"
        SHIPPED = "SHIPPED", "In Transit"
        DELIVERED = "DELIVERED", "Delivered"
        COMPLETED = "COMPLETED", "Completed & Released"
        CANCELLED = "CANCELLED", "Cancelled"

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    # Change this line:
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sales",
        null=True,  # Add this
        blank=True,  # Add this
    )
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def confirm_delivery(self):
        """When the buyer confirms they got the fish, release the cash."""
        if self.status == self.OrderStatus.DELIVERED:
            self.status = self.OrderStatus.COMPLETED
            self.save()
            # Trigger the escrow release
            if hasattr(self, "escrow"):
                self.escrow.release_funds()
