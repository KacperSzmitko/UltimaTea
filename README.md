

# About the project
This project is a web aplication, used to control a tea machine we constructed. Current features of the application:
* Account creation
* Changing password via email (emails are sended by Celery workers)
* Logging in
* Creating new tea recipe
* Advanced recipes filtering (in the future we will try to use ElasticSearch)
* Deleting and modifying existing tea recipes
* Browsing recipes published by other users
* Coping recipes created by other users
* Tracking the status of a machine
* Editing user profile

# Technologies used
* Python and Django as backend engine
* CSS, HTML and Bootstrap 
* Celery with Redis as broker used for example to asynchronous mail sending, newletter sending etc.
* MySQL as database
* Adobe XD to create desing projects


# Setup
1. Install python 3.9
2. Run: pipenv shell
3. Run: pipenv install
4. Go to src folder
5. Run server: python manage.py runserver
or if using Vscode run debug

# Run Celery
cd src
celery -A UltimaTea worker -l info -P gevent





