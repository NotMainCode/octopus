"""URLs configuration of the 'tokens' endpoints of 'Api' app v1."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.v1.drf_spectacular.custom_decorators import (
    activate_drf_spectacular_view_decorator,
)

urlpatterns = [
    path(
        "refresh/",
        activate_drf_spectacular_view_decorator(TokenRefreshView.as_view()),
        name="refresh_token",
    ),
]
