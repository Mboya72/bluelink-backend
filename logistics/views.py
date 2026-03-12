from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import TransportJob, GPSLog
from .serializers import TransportJobSerializer # You'll need to create this

class DriverLocationUpdateView(generics.UpdateAPIView):
    """
    Allows ONLY the assigned driver to update their current GPS coordinates.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = TransportJob.objects.all()

    def perform_update(self, serializer):
        # Security check: Is this the driver assigned to this job?
        job = self.get_object()
        if job.driver != self.request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        # Save the new location
        instance = serializer.save()
        
        # Also log it for Trip Playback
        GPSLog.objects.create(
            job=instance,
            lat=instance.current_lat,
            lng=instance.current_lng
        )

class BuyerTrackOrderView(generics.RetrieveAPIView):
    """
    Allows ONLY the buyer of the order to see the live location.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = TransportJob.objects.all()

    def get(self, request, *args, **kwargs):
        job = self.get_object()
        # Security check: Is the logged-in user the buyer of this order?
        if job.order.buyer != request.user:
            return Response({"error": "You cannot track this order"}, status=status.HTTP_403_FORBIDDEN)
            
        return super().get(request, *args, **kwargs)