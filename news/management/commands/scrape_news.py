import os

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import NewsArticle
from ...services.scraper import scrape_channels


class Command(BaseCommand):

    help = "Scrape news articles from Channels TV"

    def handle(self, *args, **kwargs):
        created_count = 0
        skipped_count = 0

        def save_article(item):
            nonlocal created_count, skipped_count

            _, created = NewsArticle.objects.get_or_create(
                url=item['URL'],
                defaults={
                    "title": item['Title'],
                    "content": item['Content'],
                    "source": item['Source'],
                    "published_at": item['Published_at'] or timezone.now(),
                },
            )
            if created:
                created_count += 1
                self.stdout.write(f"  SAVED: {item['Title']}")
            else:
                skipped_count += 1
                self.stdout.write(f"  EXISTS: {item['Title']}")

        scrape_channels(save_callback=save_article)

        self.stdout.write(
            self.style.SUCCESS(
                f"Done — {created_count} new, {skipped_count} already existed"
            )
        )