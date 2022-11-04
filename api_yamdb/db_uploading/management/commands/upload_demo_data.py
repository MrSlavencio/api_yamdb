from django.core.management.base import BaseCommand
from ._csv_upload import clean_db, upload_data


class Command(BaseCommand):
    help = 'You can use this command to upload demo data to SQL-DB.'

    def handle(self, **options):
        if options['clean']:
            try:
                clean_db()
                print('Models data has been cleaned successfully!')
            except Exception as e:
                print('Something went wrong!')
                print(e)
        else:
            try:
                upload_data()
                print('Models data has been uploaded successfully!')
            except Exception as e:
                print('Something went wrong!')
                print(e)

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
