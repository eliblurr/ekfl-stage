release: python manage.py migrate
release: export DJANGO_SUPERUSER_PASSWORD=$ADMIN_PASSWORD
release: echo DJANGO_SUPERUSER_PASSWORD
web: gunicorn ekeycare.wsgi --log-file -