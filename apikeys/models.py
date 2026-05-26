from django.db import models
from django.conf import settings
from rest_framework_api_key.models import AbstractAPIKey

class UserApiKey(AbstractAPIKey):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="api_keys"
    )

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "User API key"
        verbose_name_plural = "User API keys"

    def __str__(self):
        return f"{self.name} (User: {self.user.username})"