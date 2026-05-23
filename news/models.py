from django.db import models



class NewsArticle(models.Model):

    title = models.CharField(max_length=500)

    content = models.TextField()

    source = models.CharField(max_length=255)

    url = models.URLField(unique=True)

    published_at = models.DateTimeField()

    processed = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title