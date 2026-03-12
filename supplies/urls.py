from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplyViewSet

router = DefaultRouter()
router.register(r'', SupplyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]