from django import forms
from django.forms import fields
from django.forms import widgets
from django.forms.forms import Form
from django.forms.widgets import EmailInput, PasswordInput, RadioSelect, TextInput
from .models import User
from django.contrib.auth.hashers import make_password,check_password
import re
from django.core.exceptions import ValidationError
from errors import Error, ErrorMessages

pattern = re.compile(r"(?=.*[?!.!\"#%&'()*+,\-\./:<>=?@\[\]\^_{}|~$])(?=.*[A-Z]).{8,255}")

class RegisterForm(forms.ModelForm):
    message = {}

    re_password = forms.CharField(  
                    max_length=255,
                    min_length=8,
                    required=True,
                    widget=PasswordInput(attrs={'class':'log-in register-re-password form-control'})
                    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            're_password',
            'password',
        ]
        widgets = {
        'username': TextInput(attrs={'class':'log-in form-control'}),
        'email': EmailInput(attrs={'class':'log-in form-control'}),
        'password': PasswordInput(attrs={'class':'log-in register-password'}),
        }

    def clean_re_password(self):
        if self.data.get("password") != self.cleaned_data.get("re_password"):
            raise ValidationError(self.message[Error.PASSWORDS_NOT_MATCH],code=Error.PASSWORDS_NOT_MATCH)       
        return self.cleaned_data.get("re_password")

    def clean_password(self,*args, **kwargs):
        password = self.cleaned_data.get("password")
        if not pattern.search(password):
            raise ValidationError(self.message[Error.WEAK_PASSWORD],code=Error.WEAK_PASSWORD)
        return make_password(self.cleaned_data.get("password"))


    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError(self.message[Error.USER_EXISTS],code=Error.USER_EXISTS)

        if len(username) < 3:
            raise ValidationError(self.message[Error.SHORT_USERNAME],code=Error.SHORT_USERNAME)
        return username


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(self.message[Error.EMAIL_EXISTS],code=Error.EMAIL_EXISTS)
        return email

    def __init__(self,lang,*args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]


class LoginForm(forms.ModelForm):
    message = {}

    email_or_username = forms.CharField(
        max_length=255,
        min_length=3,
        required=True,
        widget= TextInput(attrs={'class':'log-in form-control'}))

    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'email_or_username',
            'password',
            'remember_me',
        ]
        widgets = {
        'password': PasswordInput(attrs={'class':'log-in form-control'}),
        }

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data.get("email_or_username")
        if not User.objects.filter(username=email_or_username).exists():
            if not User.objects.filter(email=email_or_username).exists():
                raise ValidationError(self.message[Error.WRONG_LOGIN_OR_PASSWORD],code=Error.WRONG_LOGIN_OR_PASSWORD)
            self.is_mail = True
            return email_or_username
        self.is_mail = False
        return email_or_username


    def clean_password(self):
        password = self.cleaned_data.get("password")
        email_or_username = self.cleaned_data.get("email_or_username")
        hashed_password = ""
        if email_or_username is None:
            raise ValidationError(self.message[Error.WRONG_LOGIN_OR_PASSWORD],code=Error.WRONG_LOGIN_OR_PASSWORD)
        if not User.objects.filter(username=email_or_username).exists():
            hashed_password = User.objects.get(email=email_or_username)
        else:
            hashed_password = User.objects.get(username=email_or_username).password
        if check_password(password,hashed_password):
            return password
        raise ValidationError(self.message[Error.WRONG_LOGIN_OR_PASSWORD],code=Error.WRONG_LOGIN_OR_PASSWORD)

    def __init__(self,lang,*args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]
            