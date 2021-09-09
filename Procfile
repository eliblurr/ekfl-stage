release: python manage.py migrate && python manage.py createsuperuser --noinput --email $ADMIN_EMAIL --password $ADMIN_PASSWORD
web: gunicorn ekeycare.wsgi --log-file -