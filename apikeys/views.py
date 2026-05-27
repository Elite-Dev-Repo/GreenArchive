from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserApiKey
from .serializers import UserApiKeySerializer

class CreateAPIKeyView(ListCreateAPIView):
    serializer_class = UserApiKeySerializer
    permission_classes = [IsAuthenticated]  # <--- This prevents AnonymousUser errors
    
    def get_queryset(self):
        # Now safe because permission_classes ensures self.request.user is a User
        return UserApiKey.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        # 1. Generate the key
        api_key, key = UserApiKey.objects.create_key(
            name=request.data.get("name"), 
            user=request.user
        )

        # 2. Return the key in the response
        return Response({
            "name": api_key.name,
            "key": key,
            "created": api_key.created_at
        }, status=status.HTTP_201_CREATED)