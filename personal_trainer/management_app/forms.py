from django import forms
from django.core.exceptions import ValidationError
from .models import User, MacroElements, Reports, Photos, Exercises, PlanExercises
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator, URLValidator


class LoginUserForm(forms.Form):
    email = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        email = cd.get('email')

        try:
            validator_email = EmailValidator()
            validator_email(email)
        except ValidationError:
            self.add_error('email', 'Enter valid email')

        return cd
