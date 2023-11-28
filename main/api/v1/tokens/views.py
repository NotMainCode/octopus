"""Views for the endpoints 'tokens' of 'Api' application v1."""

from rest_framework_simplejwt.views import TokenRefreshView

from api.v1.drf_spectacular.custom_decorators import get_drf_spectacular_view_decorator


@get_drf_spectacular_view_decorator("tokens")
class CustomTokenRefreshView(TokenRefreshView):
    """Update tokens.

    Class is created to generate API documentation.
    """
