import pandas as pd

from django.core.management.base import BaseCommand

from ...models import Question




class Command(BaseCommand):

    help = "Import quiz questions from CSV"

    def handle(self, *args, **kwargs):

        df = pd.read_csv("nigeria_quiz_2000.csv")

        questions = [
            Question(
                question=row["question"],
                option_a=row["option_a"],
                option_b=row["option_b"],
                option_c=row["option_c"],
                option_d=row["option_d"],
                correct_answer=row["correct_answer"],
                category=row["category"],
                difficulty=row["difficulty"],
                source=row.get("source", ""),
            )
            for _, row in df.iterrows()
        ]
        Question.objects.bulk_create(questions)

        self.stdout.write(
            self.style.SUCCESS(
                "Questions imported successfully!"
            )
        )