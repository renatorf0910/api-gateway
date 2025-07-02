from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import AdminOnlyHelloView, hello_view

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', hello_view, name='hello_view'),
    path('hello-admin/', AdminOnlyHelloView.as_view(), name='hello-admin'),
]
