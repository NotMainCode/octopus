"""URLs configuration of the 'tokens' endpoints of 'Api' app v1."""
from django.urls import path

from api.v1.tokens.views import CustomTokenRefreshView

urlpatterns = [
    path("refresh/", CustomTokenRefreshView.as_view(), name="refresh_token"),
]
