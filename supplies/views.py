from rest_framework import viewsets, permissions
from .models import Supply
from .serializers import SupplySerializer

class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the vendor to the logged-in user
        serializer.save(vendor=self.request.user)