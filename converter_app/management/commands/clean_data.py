from django.core.management.base import BaseCommand, CommandError
from converter_app.models import Document
from django.conf import settings
from pathlib import Path


class Command(BaseCommand):
    help = 'Clean obsolete files and DB records'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # Delete all records about converted files
        Document.objects.all().delete()

        docs_to_rem = Path(settings.MEDIA_ROOT + '/documents/').glob('*.txt')
        conv_to_rem = Path(settings.MEDIA_ROOT + '/gift_converted/').glob('*.txt')

        try:
            for doc in docs_to_rem:
                doc.unlink(missing_ok=True)
            for conv in conv_to_rem:
                conv.unlink(missing_ok=True)
        except FileNotFoundError as e:
            print(e)

        self.stdout.write(self.style.SUCCESS('Files and records deleted'))
