from django.shortcuts import render
from .serializers import NewsArticleSerializer
from rest_framework.generics import ListAPIView
from .models import NewsArticle
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response




# Create your views here.

class NewsArticleListView(ListAPIView):
    serializer_class = NewsArticleSerializer
    queryset = NewsArticle.objects.all()
    filterset_fields = ['processed']
    permission_classes = [IsAdminUser]

