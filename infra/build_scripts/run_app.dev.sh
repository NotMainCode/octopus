python manage.py migrate --no-input
python manage.py loaddata companies.json users.json
gunicorn octopus.wsgi:application --bind 0:8008
