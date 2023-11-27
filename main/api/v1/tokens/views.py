"""Views for the endpoints 'tokens' of 'Api' application v1."""
from rest_framework_simplejwt.views import TokenRefreshView

from api.v1.drf_spectacular.custom_decorators import (
    activate_drf_spectacular_view_decorator,
)


@activate_drf_spectacular_view_decorator
class CustomTokenRefreshView(TokenRefreshView):
    """Update tokens.

    Class is created to generate API documentation.
    """
