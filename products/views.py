from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-created_at') 
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug', 'location', 'price_per_kg']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()] # Only logged-in users can post
        return [permissions.AllowAny()] # Anyone can browse the market

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)