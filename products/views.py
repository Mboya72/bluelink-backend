from requests import Response
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from logistics.permissions import IsFisherman

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
        
    def create(self, request, *args, **kwargs):
        category = request.data.get('category')
        
        # If the user is trying to post Fish, check if they are a Fisherman
        if category == 'FISH' and not IsFisherman().has_permission(request, self):
            return Response(
                {"detail": "Only verified Fishermen can post fish products."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)