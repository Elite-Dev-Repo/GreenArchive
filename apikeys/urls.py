from django.urls import path
from .views import CreateAPIKeyView, DeleteApiKeyView




urlpatterns = [
    path('create-api-key/', CreateAPIKeyView.as_view(), name='create-api-key'),
    path('delete-api-key/<str:id>/', DeleteApiKeyView.as_view(), name='delete-api-key'), 
]