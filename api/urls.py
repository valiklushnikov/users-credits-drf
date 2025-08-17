from api.spectacular.urls import urlpatterns as doc_urls
from apps.accounts.urls import urlpatterns as account_urls
from apps.credits.urls import urlpatterns as credits_urls


app_name = "api"

urlpatterns = []

urlpatterns += doc_urls
urlpatterns += account_urls
urlpatterns += credits_urls
