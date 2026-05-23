from django.shortcuts import render
from .serializers import QuestionSerializer
from rest_framework.generics import ListAPIView
from .models import Question
from rest_framework.response import Response


# Create your views here.

class QuestionListView(ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    filterset_fields = ['category', 'difficulty']