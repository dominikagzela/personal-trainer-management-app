from django import forms
from django.core.exceptions import ValidationError
from .models import User, MacroElements, Reports, Photos, Exercises, PlanExercises, TRAINING
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator, URLValidator


class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=265)
    password = forms.CharField(widget=forms.PasswordInput)


class PlanExercisesForm(forms.ModelForm):
    # training_number = forms.ChoiceField(choices=TRAINING)
    # exercise = forms.ModelChoiceField(queryset=Exercises.objects.all().values_list('name', flat=True).distinct())
    exercise = forms.ModelChoiceField(queryset=Exercises.objects.all(), to_field_name='name', required=False)

    class Meta:
        model = PlanExercises
        fields = [
            'exercise',
            'series',
            'repeat',
            'TUT',
        ]


