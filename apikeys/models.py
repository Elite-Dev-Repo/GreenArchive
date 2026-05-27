from django.db import models
from django.conf import settings
from rest_framework_api_key.models import AbstractAPIKey
from django.contrib.auth.models import User

class UserApiKey(AbstractAPIKey):
    user = models.ForeignKey(User, 
        on_delete=models.CASCADE, 
        related_name="api_keys"
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    class Meta(AbstractAPIKey.Meta):
        verbose_name = "User API key"
        verbose_name_plural = "User API keys"

    def __str__(self):
        return f"{self.name} (User: {self.user.username})"