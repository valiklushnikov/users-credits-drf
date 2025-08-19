import re
import csv

from datetime import datetime
from django.db import transaction
from django.utils.timezone import make_aware

from apps.credits.models import Plans


def parse_date_field(value):
    if isinstance(value, str):
        if value.strip() == "":
            return None
        value = value.strip()
        date_pattern = re.compile(
            r"^\d{2}\.\d{2}\.\d{4}$|^\d{4}-\d{2}-\d{2}$|^\d{2}/\d{2}/\d{4}$"
        )
        if date_pattern.match(value):
            if date_pattern.match(value):
                if "." in value:
                    fmt = "%d.%m.%Y"
                elif "-" in value:
                    fmt = "%Y-%m-%d"
                elif "/" in value:
                    fmt = "%d/%m/%Y"
            dt = datetime.strptime(value, fmt)
            return make_aware(dt)
        return value
    return value


def parse_csv_bulk_create_from_file(command=None, path=None, model=None, **kwargs):
    model_fields = {field.name for field in model._meta.get_fields() if field.concrete}
    command.stdout.write(f"Importing {path}...")
    instances_to_create = []
    extra_fields = {}
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                filtered_data = {}
                for key, value in row.items():
                    if key == "id":
                        continue
                    if "id" in key:
                        extra_fields[key] = value
                    if key in model_fields:
                        filtered_data[key] = parse_date_field(value)
                instances_to_create.append(model(**extra_fields, **filtered_data))
    except FileNotFoundError:
        raise FileNotFoundError({"message": f"File {path} not found"})
    with transaction.atomic():
        model.objects.bulk_create(instances_to_create, batch_size=500)
    command.stdout.write(
        command.style.SUCCESS(
            f"Downloaded: {len(instances_to_create)} instances from {path}"
        )
    )


def check_plans_exists(period, category_id):
    date = parse_date_field(period)
    return Plans.objects.filter(period=date, category_id=category_id).exists()


def start_with_first_day(period):
    return period.startswith("01")


def is_null_sum(value):
    if value.strip() == "":
        return True
    return False
