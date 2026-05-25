from django.urls import path
from .views import NewsArticleListView



urlpatterns = [
    path('', NewsArticleListView.as_view(), name='news-list'),
    
]