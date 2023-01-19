from django.core.management.base import BaseCommand

from skills_review.skills import taxonomy


class Command(BaseCommand):
    def handle(self, *args, **options):
        taxonomy.create_job_title_embeddings()
        print("Initialised taxonomy")  # noqa
