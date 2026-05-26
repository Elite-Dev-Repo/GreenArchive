from django.urls import path
from .views import CreateAPIKeyView


urlpatterns = [
    path('create-api-key/', CreateAPIKeyView.as_view(), name='create-api-key'),
    
]