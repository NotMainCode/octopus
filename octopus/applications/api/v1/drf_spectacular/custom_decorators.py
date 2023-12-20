"""Custom decorators for drf-spectacular."""

from django.conf import settings


def get_drf_spectacular_view_decorator(endpoint_group):
    def activate_drf_spectacular_view_decorator(view):
        """If DEBUG=True, select view decorator for specified view."""
        if not settings.DEBUG:
            return view

        from applications.api.v1.drf_spectacular.view_decorators import VIEW_DECORATORS

        view_name = (
            view.view_class.__name__
            if view.__class__.__name__ == "function"
            else view.__name__
        )
        return VIEW_DECORATORS[endpoint_group][view_name](view)

    return activate_drf_spectacular_view_decorator
