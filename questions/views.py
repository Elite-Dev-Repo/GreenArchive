from django.shortcuts import render
from .serializers import QuestionSerializer
from rest_framework.generics import ListAPIView
from .models import Question
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from rest_framework.permissions import IsAdminUser, IsAuthenticated






# Create your views here.

class QuestionListView(ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    filterset_fields = ['category', 'difficulty']
    permission_classes = [HasAPIKey]



class CreateAPIKeyView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        name = request.data.get("name", "default")
        api_key, key = APIKey.objects.create_key(name=name)
        return Response({"api_key": key})
