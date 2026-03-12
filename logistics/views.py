from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Route, Truck, TransportJob, GPSLog
from .serializers import RouteSerializer, TruckSerializer, TransportJobSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action  # <--- Add this line
from rest_framework.response import Response  # Ensure this is also imported

class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Returns a summary of truck statistics for the seller.
        URL: /api/logistics/trucks/summary/
        """
        total = self.get_queryset().count()
        available = self.get_queryset().filter(is_available=True).count()
        
        return Response({
            "total_trucks": total,
            "available_trucks": available,
            "in_transit": total - available,
            "monthly_revenue": 0.00  # You can link your Finance model here later
        })

class TransportJobViewSet(viewsets.ModelViewSet):
    queryset = TransportJob.objects.all()
    serializer_class = TransportJobSerializer
    permission_classes = [permissions.IsAuthenticated]

class DriverLocationUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TransportJob.objects.all()
    serializer_class = TransportJobSerializer

    def perform_update(self, serializer):
        job = self.get_object()
        # Security check: ensures only the linked driver can update location
        if job.vehicle.driver != self.request.user:
            raise PermissionDenied("Unauthorized: You are not the assigned driver.")
        
        instance = serializer.save()
        
        GPSLog.objects.create(
            job=instance,
            lat=instance.current_lat,
            lng=instance.current_lng
        )

class BuyerTrackOrderView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TransportJob.objects.all()
    serializer_class = TransportJobSerializer

    def get_object(self):
        job = super().get_object()
        if job.order.buyer != self.request.user:
            raise PermissionDenied("Unauthorized: You cannot track this order.")
        return job
    
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer