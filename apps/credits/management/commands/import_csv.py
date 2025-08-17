import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.credits.models import Credits, Dictionary, Plans, Payments

from utils import parse_csv_bulk_create_from_file


User = get_user_model()


class Command(BaseCommand):
    help = "Importing csv files from data folder"

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, "data")
        users_path = os.path.join(data_dir, "users.csv")
        credits_path = os.path.join(data_dir, "credits.csv")
        dictionary_path = os.path.join(data_dir, "dictionary.csv")
        payments_path = os.path.join(data_dir, "payments.csv")
        data_to_parse = [
            {
                "path": users_path,
                "model": User,
            },
            {
                "path": credits_path,
                "model": Credits,
            },
            {
                "path": dictionary_path,
                "model": Dictionary,
            },
            {
                "path": payments_path,
                "model": Payments,
            },
        ]
        for data in data_to_parse:
            path = data.get("path")
            model = data.get("model")
            parse_csv_bulk_create_from_file(self, path=path, model=model)

