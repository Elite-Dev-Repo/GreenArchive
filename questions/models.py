from django.db import models





class Question(models.Model):

    CATEGORY_CHOICES = [
        ("history", "History"),
        ("politics", "Politics"),
        ("sports", "Sports"),
        ("culture", "Culture"),
        ("government", "Government"),
        ("current_affairs", "Current Affairs"),
    ]

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(max_length=1)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        db_index=True
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        db_index=True
    )

    source = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["category", "difficulty"]),
        ]

    def __str__(self):
        return self.question
    
