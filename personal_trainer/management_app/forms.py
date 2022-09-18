from django import forms
from django.core.exceptions import ValidationError
from .models import (
    User,
    MacroElements,
    Reports, Photos,
    Exercises,
    PlanExercises,
    TRAINING,
    PracticalTips,
)
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator, URLValidator


class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=265)
    password = forms.CharField(widget=forms.PasswordInput)


class PracticalTipForm(forms.ModelForm):
    class Meta:
        model = PracticalTips
        fields = ['tip']
        labels = {'tip': 'Opis'}


class MacroElementsForm(forms.ModelForm):
    calories = forms.IntegerField(label='Kalorie (kcal)', min_value=1000, max_value=8000, step_size=1)
    protein = forms.IntegerField(label='Białko (g)', min_value=1, max_value=800, step_size=1)
    fat = forms.IntegerField(label='Tłuszcze (g)', min_value=1, max_value=800, step_size=1)
    carb = forms.IntegerField(label='Węglowodany (g)', min_value=1, max_value=1500, step_size=1)

    class Meta:
        model = MacroElements
        exclude = ['user']


class ExercisesForm(forms.ModelForm):
    class Meta:
        model = Exercises
        fields = [
            'name',
            'description',
            'url',
        ]
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'url': 'Adres url',
        }


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


class ReportForm(forms.ModelForm):
    weight = forms.IntegerField(label='Waga (kg)', min_value=20, max_value=300, step_size=1)
    waist = forms.IntegerField(label='Talia (cm)', min_value=20, max_value=300, step_size=1)
    stomach = forms.IntegerField(label='Brzuch (cm)', min_value=20, max_value=300, step_size=1)
    hip = forms.IntegerField(label='Biodra (cm)', min_value=20, max_value=300, step_size=1)
    thigh = forms.IntegerField(label='Udo (cm)', min_value=20, max_value=300, step_size=1)
    training_first = forms.BooleanField(label='Trening 1', required=False)
    training_second = forms.BooleanField(label='Trening 2', required=False)
    training_third = forms.BooleanField(label='Trening 3', required=False)
    training_fourth = forms.BooleanField(label='Trening 4', required=False)
    comments = forms.CharField(widget=forms.Textarea, label='Komentarz')

    class Meta:
        model = Reports
        exclude = ['user', 'created_date']
