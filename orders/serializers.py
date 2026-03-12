from rest_framework import serializers
from .models import Order
from payments.models import Escrow
from products.models import Product

class OrderCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.FloatField(write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'product_id', 'quantity', 'total_amount', 'status']
        read_only_fields = ['total_amount', 'status']

    def create(self, validated_data):
        user = self.context['request'].user
        product = Product.objects.get(id=validated_data['product_id'])
        quantity = validated_data['quantity']
        total_price = product.price_per_kg * quantity

        # 1. Create the Order
        order = Order.objects.create(
            buyer=user,
            seller=product.owner,
            total_amount=total_price,
            status=Order.OrderStatus.PENDING
        )

        # 2. Initialize Escrow (Funds are PENDING until M-Pesa confirms)
        Escrow.objects.create(
            order=order,
            buyer=user,
            seller=product.owner,
            amount=total_price,
            status=Escrow.Status.HELD
        )

        return order