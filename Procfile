release: python manage.py migrate
web: gunicorn kuropoly.wsgi
worker: python manage.py runworker channel_layer