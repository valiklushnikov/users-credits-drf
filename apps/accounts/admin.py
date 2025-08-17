from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("login", "password")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "registration_date")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "login",
                    "password",
                ),
            },
        ),
    )
    list_display = (
        "id",
        "login",
        "last_login",
        "registration_date",
    )

    list_display_links = ("login",)
    list_filter = (
        "is_staff",
        "is_superuser",
    )
    search_fields = ("login",)
    ordering = ("id", "registration_date")
    readonly_fields = ("last_login", "registration_date")
