import sys
import logging
from django.core.management.base import BaseCommand
from ._csv_upload import clean_db, upload_data


class Command(BaseCommand):
    help = 'You can use this command to upload demo data to SQL-DB.'

    def handle(self, **options):
        if options['clean']:
            try:
                clean_db()
                logging.info('Models data has been cleaned successfully!')
            except Exception as e:
                logging.error(f'Models data has not been cleaned: {e}')
        else:
            try:
                upload_data()
                logging.info('Models data has been uploaded successfully!')
            except Exception as e:
                logging.error(f'Models data has not been uploaded: {e}')

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--upload',
            action='store_true',
            default=False,
            help='Uploading data to SQL-DB'
        )
        parser.add_argument(
            '-c',
            '--clean',
            action='store_true',
            default=False,
            help='Deleting data in SQL-DB'
        )


logging.basicConfig(
    format=('%(asctime)s [%(levelname)s] %(message)s'),
    level=logging.INFO
)

logging.StreamHandler(sys.stdout)
