from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TruckViewSet, 
    TransportJobViewSet, 
    DriverLocationUpdateView, 
    BuyerTrackOrderView
)

# 1. Register ViewSets with the Router
router = DefaultRouter()
router.register(r'trucks', TruckViewSet, basename='truck')
router.register(r'jobs', TransportJobViewSet, basename='transport-job')

urlpatterns = [
    # 2. Include the Router URLs (trucks and general jobs)
    path('', include(router.urls)),

    # 3. Add the specific Generic Views
    # Update location: api/logistics/jobs/<id>/update-location/
    path('jobs/<int:pk>/update-location/', 
         DriverLocationUpdateView.as_view(), 
         name='driver-update-location'),

    # Track order: api/logistics/jobs/<id>/track/
    path('jobs/<int:pk>/track/', 
         BuyerTrackOrderView.as_view(), 
         name='buyer-track-order'),
]