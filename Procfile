release: python manage.py makemigrations && python manage.py migrate --fake-initial && python manage.py migrate
web: gunicorn gaming_platform.wsgi --log-file -