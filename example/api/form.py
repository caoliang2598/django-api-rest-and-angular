__author__ = 'caoliang'
from django import forms
from django.contrib.auth.models import User
from djangular.forms.angular_model import NgModelFormMixin
class LoginForm(NgModelFormMixin,forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
