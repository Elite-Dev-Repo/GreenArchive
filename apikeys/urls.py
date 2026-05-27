from django.urls import path
from .views import CreateAPIKeyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('create-api-key/', CreateAPIKeyView.as_view(), name='create-api-key'),
    
    
]