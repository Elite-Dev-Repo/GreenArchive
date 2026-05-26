from rest_framework import serializers
from .models import UserApiKey


class UserApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApiKey
        fields = ['name','user', 'created_at']

