from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicKeyViewSet, ChatViewSet

router = DefaultRouter()
router.register(r'public-keys', PublicKeyViewSet, basename='public-key')
router.register(r'messages', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]