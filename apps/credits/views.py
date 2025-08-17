import csv

from django.contrib.auth import get_user_model
from django.db.models import (
    BooleanField,
    Sum,
    Q,
    Case,
    When,
    Value,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
)
from . import models
from . import serializers
from utils import (
    check_plans_exists,
    start_with_first_day,
    is_null_sum,
    parse_date_field,
)

User = get_user_model()


@extend_schema_view(
    get=extend_schema(
        summary="Get user credit information",
        tags=["Credits"],
    ),
)
class CreditsAPIView(APIView):
    serializer_class = serializers.CreditsSerializer

    def get(self, request, user_id):
        if not User.objects.filter(pk=user_id).exists():
            return Response(
                {"message": f"User with id: {user_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        credits = (
            models.Credits.objects.filter(user_id=user_id)
            .annotate(
                is_closed=Case(
                    When(actual_return_date__isnull=False, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
            )
            .annotate(
                total_payments=Sum("payments__sum"),
                filter=Q(actual_return_date__isnull=True),
            )
            .annotate(
                payments_body=Sum(
                    "payments__sum",
                    filter=Q(payments__type__name="тіло")
                    & Q(actual_return_date__isnull=True),
                )
            )
            .annotate(
                payments_percent=Sum(
                    "payments__sum",
                    filter=Q(payments__type__name="відсотки")
                    & Q(actual_return_date__isnull=True),
                )
            )
        )
        serializer = self.serializer_class(credits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        summary="Upload plans",
        tags=["Credits"],
    ),
)
class UploadAPIView(APIView):
    serializer_class = serializers.UploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def add_errors_test(errors, key, message, item):
        if key not in errors:
            errors[key] = {"message": message, "invalid_items": []}
        errors[key]["invalid_items"].append(item)

    def post(self, request):
        file_uploaded = request.FILES.get("file_uploaded")
        decoded_file = file_uploaded.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file, delimiter="\t")

        plans_to_create = []
        errors = {}

        for row in reader:
            period = row.get("period")
            category_id = row.get("category_id")
            amount = row.get("sum")
            if check_plans_exists(period, category_id):
                UploadAPIView.add_errors_test(
                    errors,
                    "invalid_plans",
                    "Already existing plans",
                    {"period": period, "category_id": category_id},
                )
            if not start_with_first_day(period):
                UploadAPIView.add_errors_test(
                    errors,
                    "invalid_date",
                    "Invalid date. Must start at first day of month",
                    {"period": period},
                )
            if is_null_sum(amount):
                UploadAPIView.add_errors_test(
                    errors,
                    "invalid_sum",
                    "Invalid sum. Sum can not be null",
                    {"period": period, "sum": amount},
                )
            plans_to_create.append(
                models.Plans(
                    period=parse_date_field(period), category_id=category_id, sum=amount
                )
            )
        if errors:
            return Response(
                {
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        models.Plans.objects.bulk_create(plans_to_create, batch_size=500)
        return Response(
            {"message": "Plans added successfully"}, status=status.HTTP_201_CREATED
        )
