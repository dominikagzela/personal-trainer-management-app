from django import forms
from django.core.exceptions import ValidationError
from .models import User, MacroElements, Reports, Photos, Exercises, PlanExercises
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator, URLValidator


class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=265)
    password = forms.CharField(widget=forms.PasswordInput)

