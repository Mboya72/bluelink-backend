from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Truck, TransportJob, GPSLog
from .serializers import TruckSerializer, TransportJobSerializer

class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

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