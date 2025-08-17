from django.contrib import admin
from apps.credits import models


@admin.register(models.Credits)
class CreditsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "issuance_date",
        "return_date",
        "actual_return_date",
        "body",
        "percent",
    )


@admin.register(models.Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Plans)
class PlansAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "period",
        "sum",
    )


@admin.register(models.Payments)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = (
        "sum",
        "payment_date",
        "credit",
        "type"
    )
