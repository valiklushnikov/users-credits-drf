from django.urls import path
from . import views

app_name = "credits"

urlpatterns = [
    path("user_credits/<int:user_id>", views.CreditsAPIView.as_view(), name="user_credits"),
    path("plans_insert/", views.UploadAPIView.as_view(), name="plans_insert"),
]
