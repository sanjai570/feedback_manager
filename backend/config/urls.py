from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Removed in favor of apps.users.urls
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('apps.users.urls')),
    path('api/resources/', include('apps.resources.urls')),
    path('api/bookings/', include('apps.bookings.urls')),
]
