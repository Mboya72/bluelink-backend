from django.contrib import admin
from django.urls import path, include  # <--- Ensure 'path' is here
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from bluelink import settings
from users.views import RegisterView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth Endpoints
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/chat/', include('communication.urls')),
    path('api/products/', include('products.urls')),
    path('api/logistics/', include('logistics.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/supplies/', include('supplies.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)