from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["id","question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "category", "difficulty", "source",]