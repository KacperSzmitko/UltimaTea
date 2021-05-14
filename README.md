SETUP
1. Install python 3.9
2. Run: pipenv shell
3. Run: pipenv install
4. Go to src folder
5. Run server: python manage.py runserver

# UltimaTea



CELERY
cd src
celery -A UltimaTea worker -l info -P gevent
