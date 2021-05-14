from celery.utils.log import get_task_logger
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
logger = get_task_logger(__name__)

@shared_task(name="send_mails")
def send_mails(context,receiver):
    html_message=render_to_string("login_register/mail.html",context)
    plain_message = strip_tags(html_message)
    return send_mail(
        "Zmiana hasła",
        plain_message,
        settings.EMAIL_HOST_USER,
        [receiver],False,
        html_message=html_message)

# Faster 0.1 s
@shared_task(name="save")
def save(form):
    return User.objects.create_user(form['username'],form['email'],form['password'])

