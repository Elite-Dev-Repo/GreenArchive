from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from .models import UserApiKey

@admin.register(UserApiKey)
class UserApiKeyAdmin(APIKeyModelAdmin):
    """
    Subclassing APIKeyModelAdmin is required so Django Admin knows to call 
    our custom .assign_key() logic instead of just calling a standard .save()
    """
    pass



