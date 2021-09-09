release: python manage.py migrate
release: python manage.py createsuperuser --noinput --email $ADMIN_EMAIL
web: gunicorn ekeycare.wsgi --log-file -