from django.conf import settings
from django.core.files.base import File
from django.core.management.base import BaseCommand

from skills_review.skills.data import process_file


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename")

    def handle(self, *args, **options):
        filename = options["filename"]
        filepath = settings.BASE_DIR / filename
        with filepath.open() as f:
            file_object = File(f)
            lines = process_file(file_object)
        print(lines[0])
