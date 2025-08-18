from django.core.validators import FileExtensionValidator
from django.utils.timezone import now

from rest_framework import serializers
from apps.credits import models


class CreditsSerializer(serializers.ModelSerializer):
    is_closed = serializers.SerializerMethodField()
    days_overdue = serializers.SerializerMethodField()
    total_payments = serializers.SerializerMethodField()
    payments_body = serializers.SerializerMethodField()
    payments_percent = serializers.SerializerMethodField()

    class Meta:
        model = models.Credits
        fields = [
            "issuance_date",
            "is_closed",
            "actual_return_date",
            "body",
            "percent",
            "total_payments",
            "return_date",
            "days_overdue",
            "payments_body",
            "payments_percent",
        ]

    def get_is_closed(self, obj) -> bool:
        return getattr(obj, "is_closed", obj.is_closed)

    def get_days_overdue(self, obj) -> int:
        if obj.actual_return_date is None:
            return (now().date() - obj.return_date).days
        return 0

    def get_payments_body(self, obj) -> float:
        return getattr(obj, "payments_body", obj.payments_body)

    def get_payments_percent(self, obj) -> float:
        return getattr(obj, "payments_percent", obj.payments_percent)

    def get_total_payments(self, obj) -> float | None:
        if obj.actual_return_date:
            return getattr(obj, "total_payments", obj.total_payments)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_closed:
            data.pop("return_date", None)
            data.pop("days_overdue", None)
            data.pop("payments_body", None)
            data.pop("payments_percent", None)
        else:
            data.pop("actual_return_date", None)
            data.pop("total_payments", None)
        return data


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )

    class Meta:
        fields = ["file_uploaded"]
