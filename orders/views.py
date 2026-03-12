from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderCreateSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def get_queryset(self):
        # Users only see their own orders
        return Order.objects.filter(buyer=self.request.user)

    def perform_create(self, serializer):
        serializer.save()