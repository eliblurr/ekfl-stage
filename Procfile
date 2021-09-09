release: python manage.py migrate
release: export DJANGO_SUPERUSER_PASSWORD=$ADMIN_PASSWORD
release: echo DJANGO_SUPERUSER_PASSWORD
release: python manage.py createsuperuser --noinput --email $ADMIN_EMAIL
web: gunicorn ekeycare.wsgi --log-file -