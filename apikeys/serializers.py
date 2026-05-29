from rest_framework import serializers
from .models import UserApiKey


class UserApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApiKey
        fields = ['id','name','user', 'created_at']

