# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyTokenObtainPairView, UserViewSet, RegisterView

router = DefaultRouter()
# Registering with r'' means the 'me' action becomes /api/users/me/
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]