"""View decorators of endpoint groups for use in documentation."""

from api.v1.drf_spectacular.auth.view_decorators import AUTH_VIEW_DECORATORS
from api.v1.drf_spectacular.companies.view_decorators import COMPANIES_VIEW_DECORATORS
from api.v1.drf_spectacular.info.view_decorators import INFO_VIEW_DECORATORS
from api.v1.drf_spectacular.tokens.view_decorators import TOKENS_VIEW_DECORATORS
from api.v1.drf_spectacular.users.view_decorators import USERS_VIEW_DECORATORS

VIEW_DECORATORS = {
    "auth": AUTH_VIEW_DECORATORS,
    "companies": COMPANIES_VIEW_DECORATORS,
    "info": INFO_VIEW_DECORATORS,
    "tokens": TOKENS_VIEW_DECORATORS,
    "users": USERS_VIEW_DECORATORS,
}
