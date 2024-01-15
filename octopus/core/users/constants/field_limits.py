"""Field limits for models of 'Users' application."""


FIELD_LIMITS_USERS_APP = {
    "user_full_name_min_char": 2,
    "user_full_name_max_char": 30,
    "email_max_char": 254,
    "password_min_char": 8,
    "password_max_char": 30,
    "password_hash_max_char": 128,
}
