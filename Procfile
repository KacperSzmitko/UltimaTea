web: sh -c 'cd src && gunicorn UltimaTea.wsgi:application'
release: sh -c 'cd src && python manage.py migrate'
worker: sh -c 'cd src && celery -A UltimaTea worker' 