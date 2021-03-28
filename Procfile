release: python manage.py migrate --noinput
web: daphne kuropoly.asgi:application --port $PORT --bind 0.0.0.0