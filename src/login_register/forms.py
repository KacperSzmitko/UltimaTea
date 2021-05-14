from django import forms
from django.forms import fields
from django.forms import widgets
from django.forms.forms import Form
from django.forms.widgets import EmailInput, PasswordInput, RadioSelect, TextInput
#from .models import User
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
import re
from django.core.exceptions import ValidationError
from errors import Error, ErrorMessages
from django.contrib.auth.forms import UserCreationForm

pattern = re.compile(r"(?=.*[?!.!\"#%&'()*+,\-\./:<>=?@\[\]\^_{}|~$])(?=.*[A-Z]).{8,255}")

class RegisterForm(UserCreationForm):
    message = {}

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        widgets = {
        'username': TextInput(attrs={'class':'log-in '}),
        'email': EmailInput(attrs={'class':'log-in '}),
        'password1': TextInput(attrs={'class':'log-in','id':'reg_id_password','name':'password'}),
        'password2': PasswordInput(attrs={'class':'log-in', 'id':'id_re_password','name':'re_password'}),
        }

    def clean_password2(self):     
        return self.cleaned_data.get("password2")

    def clean_password1(self,*args, **kwargs):
        return self.cleaned_data.get("password1")


    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError(self.message[Error.USER_EXISTS],code=Error.USER_EXISTS)
        return username


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(self.message[Error.EMAIL_EXISTS],code=Error.EMAIL_EXISTS)
        return email

    def __init__(self,lang,*args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]


class LoginForm(forms.Form):
    message = {}

    remember_me = forms.BooleanField(required=False)
    login_username = forms.CharField(widget=TextInput(attrs={'class':'log-in ', 'id' : 'id_email_or_username','name':'email_or_username'}),required=True)
    password = forms.CharField(widget=PasswordInput(attrs={'class':'log-in ','id':'log_id_password'}),required=True)


    def clean_login_username(self):
        email_or_username = self.cleaned_data.get("login_username")
        if not User.objects.filter(username=email_or_username).exists():
            if not User.objects.filter(email=email_or_username).exists():
                raise ValidationError(self.message[Error.WRONG_LOGIN],code=Error.WRONG_LOGIN)
            self.is_mail = True
            return email_or_username
        self.is_mail = False
        return email_or_username


    def clean_password(self):
        password = self.cleaned_data.get("password")
        email_or_username = self.cleaned_data.get("login_username")
        hashed_password = ""
        if email_or_username is None:
            raise ValidationError(self.message[Error.WRONG_PASSWORD],code=Error.WRONG_PASSWORD)
        if not User.objects.filter(username=email_or_username).exists():
            hashed_password = User.objects.get(email=email_or_username).password
        else:
            hashed_password = User.objects.get(username=email_or_username).password
        if check_password(password,hashed_password):
            return password
        raise ValidationError(self.message[Error.WRONG_PASSWORD],code=Error.WRONG_PASSWORD)
    def __init__(self,lang,*args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]
            

class ResetPasswordForm(forms.Form):
    message = {}

    email = forms.EmailField(
        max_length=255,
        required=True,
        widget= TextInput(attrs={'class':'log-in '}))

    def __init__(self,lang,*args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]


class ChangePasswordForm(forms.ModelForm):

    re_password = forms.CharField(  
                    max_length=255,
                    required=True,
                    widget=PasswordInput(attrs={'class':'log-in register-re-password', 'id': 'change_re_password'})
                    )

    class Meta:
        model = User
        fields = [
            'password',
            're_password'
        ]
        widgets = {'password': PasswordInput(attrs={'class':'log-in', 'id' : "change_password"})}


    def __init__(self,lang,*args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]