python manage.py migrate --no-input
gunicorn octopus.wsgi:application --bind 0:8008
