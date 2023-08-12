from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # JWT 登录认证

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT 登录认证
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
