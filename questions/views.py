from django.shortcuts import render
from .serializers import QuestionSerializer
from rest_framework.generics import ListAPIView
from .models import Question
from rest_framework.response import Response
from rest_framework_api_key.models import APIKey
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from apikeys.permissions import HasUserAPIKey







# Create your views here.

class QuestionListView(ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    filterset_fields = ['category', 'difficulty']
    permission_classes = [HasUserAPIKey]

