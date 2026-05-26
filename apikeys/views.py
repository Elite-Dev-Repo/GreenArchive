from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import UserApiKey
from .serializers import UserApiKeySerializer
from rest_framework.response import Response
from rest_framework import status






# Create your views here.
class CreateAPIKeyView(ListCreateAPIView):
    serializer_class = UserApiKeySerializer
    
    
    def get_queryset(self):
        return UserApiKey.objects.filter(user=self.request.user)


    def post(self, request, *args, **kwargs):
        # 1. Generate the key (this returns the plaintext key)
        # We pass the user and a name for the key
        # returns key object and actual key
        api_key, key = UserApiKey.objects.create_key(
            name=request.data.get("name"), 
            user=request.user
        )

        # 2. Return the key in the response
        # IMPORTANT: You can only ever see the plaintext 'key' at this moment.
        # Once this request finishes, the plaintext is gone forever.
        return Response({
            "name": api_key.name,
            "key": key,
            "created":api_key.created_at
        }, status=status.HTTP_201_CREATED)