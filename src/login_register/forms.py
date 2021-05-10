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

    def clean_password2(self) -> str:
        return super().clean_password2()

    def __init__(self,lang,*args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]


class LoginForm(forms.Form):
    message = {}

    remember_me = forms.BooleanField(required=False)
    username = forms.CharField(widget=TextInput(attrs={'class':'log-in ', 'id' : 'id_email_or_username','name':'email_or_username'}),required=True)
    password = forms.CharField(widget=PasswordInput(attrs={'class':'log-in ','id':'log_id_password'}),required=True)

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