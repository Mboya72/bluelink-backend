from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Balance: {self.balance}"

class Escrow(models.Model):
    class Status(models.TextChoices):
        HELD = 'HELD', 'Funds Held'
        RELEASED = 'RELEASED', 'Funds Released to Seller'
        REFUNDED = 'REFUNDED', 'Funds Refunded to Buyer'
        DISPUTED = 'DISPUTED', 'Under Review'

    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='escrow')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='escrow_payments')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='escrow_earnings')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.HELD)
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)

    def release_funds(self):
        """Moves money from Escrow to the Seller's Wallet."""
        if self.status == self.Status.HELD:
            seller_wallet, created = Wallet.objects.get_or_create(user=self.seller)
            seller_wallet.balance += self.amount
            seller_wallet.save()
            self.status = self.Status.RELEASED
            self.save()

    def __str__(self):
        return f"Escrow for Order {self.order.id} - {self.status}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('PAYMENT', 'Payment'),
    )
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tx_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    reference = models.CharField(max_length=100, unique=True) # M-Pesa Receipt Number
    timestamp = models.DateTimeField(auto_now_add=True)