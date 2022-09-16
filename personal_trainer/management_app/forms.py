from django import forms
from django.core.exceptions import ValidationError
from .models import User, MacroElements, Reports, Photos, Exercises, PlanExercises, TRAINING
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator, URLValidator


class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=265)
    password = forms.CharField(widget=forms.PasswordInput)


class PlanExercisesForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=Exercises.objects.all(), label='Ćwiczenie', empty_label=None, to_field_name='name', required=False)
    series = forms.IntegerField(label='Serie', min_value=1, max_value=10, step_size=1)
    repeat = forms.IntegerField(label='Powtórzenia', min_value=1, max_value=50, step_size=1)

    class Meta:
        model = PlanExercises
        fields = [
            'exercise',
            'series',
            'repeat',
            'TUT',
        ]


