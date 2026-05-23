import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

from news.models import NewsArticle
from questions.models import Question

PROMPT = """You are a Nigerian quiz question generator. Your task:

1. Read the news article below.
2. Decide if this article is worth turning into a quiz question,
the question must be about history, very imoprtant politics, or a major milestone crime case solved.
   - WORTHY: The article contains factual, educational, or notable information (events, people, places, policies, records, etc.)
   - NOT WORTHY: The article is opinion-based, speculative, very short/trivial, or lacks concrete facts, or  does not concern nigeria, can't be taught about in schools etc.
3. If NOT worthy, set the skip field to true.
4. If worthy, set the skip field to false and populate the matching fields.

ARTICLE:
{article_content}

Return ONLY a valid JSON object matching this exact structural schema:
{{
    "skip": bool,
    "question": "str or empty string if skipping",
    "option_a": "str or empty string if skipping",
    "option_b": "str or empty string if skipping",
    "option_c": "str or empty string if skipping",
    "option_d": "str or empty string if skipping",
    "correct_answer": "A, B, C, or D or empty string if skipping",
    "category": "history, politics, sports, culture, government, or current_affairs",
    "difficulty": "easy, medium, or hard"
}}"""


class Command(BaseCommand):

    help = "Generate quiz questions from unprocessed news articles"

    def handle(self, *args, **kwargs):
        # Targeting Google AI Studio's native OpenAI-compatible gateway
        client = OpenAI(
            api_key=os.environ.get("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

        articles = NewsArticle.objects.filter(processed=False).only("content", "title", "processed")
        total = articles.count()
        self.stdout.write(f"Found {total} unprocessed articles")

        created = 0
        skipped = 0
        errors = 0

        for i, article in enumerate(articles.iterator(), 1):
            self.stdout.write(f"[{i}/{total}] {article.title[:60]}...")

            try:
                response = client.chat.completions.create(
                    model="gemini-2.5-flash", # Native Gemini 2.5 Flash model identifier
                    messages=[
                        {"role": "user", "content": PROMPT.format(article_content=article.content)},
                    ],
                    temperature=0.2,
                    response_format={"type": "json_object"} # Google natively respects this to enforce the schema layout
                )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  API error: {e}"))
                try:
                    self.stdout.write(f"    {e.body.get('error', {}).get('message', '')}")
                except Exception:
                    pass
                errors += 1
                article.processed = True
                article.delete()
                continue

            raw = response.choices[0].message.content.strip()

            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                self.stdout.write(self.style.WARNING(f"  Invalid JSON response"))
                self.stdout.write(f"    Raw: {raw[:200]}")
                errors += 1
                article.processed = True
                article.save(update_fields=["processed"])
                continue

            if not isinstance(data, dict):
                self.stdout.write(f"  SKIPPED (response: {data})")
                skipped += 1
                article.processed = True
                article.save(update_fields=["processed"])
                continue

            if data.get("skip") is True:
                self.stdout.write(f"  SKIPPED (not question-worthy)")
                skipped += 1
                article.processed = True
                article.save(update_fields=["processed"])
                continue

            required = {"question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "category", "difficulty"}
            if not required.issubset(data.keys()):
                self.stdout.write(self.style.WARNING(f"  Missing fields in response"))
                errors += 1
                article.processed = True
                article.save(update_fields=["processed"])
                continue

            Question.objects.create(
                question=data["question"],
                option_a=data["option_a"],
                option_b=data["option_b"],
                option_c=data["option_c"],
                option_d=data["option_d"],
                correct_answer=data["correct_answer"].upper(),
                category=data["category"].lower(),
                difficulty=data["difficulty"].lower(),
                source=article.title,
            )

            created += 1
            article.processed = True
            article.save(update_fields=["processed"])

            self.stdout.write(self.style.SUCCESS(f"  QUESTION CREATED: {data['question'][:60]}..."))

            # Native Gemini Free tier rates are generous (15 RPM), a 1-second pause prevents hitting them entirely
            time.sleep(1)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone — {created} created, {skipped} skipped, {errors} errors"
            )
        )