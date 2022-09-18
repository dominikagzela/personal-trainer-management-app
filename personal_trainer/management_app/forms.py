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


class AddPracticalTipForm(forms.ModelForm):
    class Meta:
        model = PracticalTips
        fields = ['tip']
        labels = {'tip': 'Wskazówka'}


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


# class ReportForm(forms.ModelForm):
#     weight = forms.IntegerField(label='Waga', min_value=20, max_value=300, step_size=1)
#     waist = forms.IntegerField(label='Talia', min_value=20, max_value=300, step_size=1)
#     stomach = forms.IntegerField(label='Brzuch', min_value=20, max_value=300, step_size=1)
#     hip = forms.IntegerField(label='Biodra', min_value=20, max_value=300, step_size=1)
#     thigh = forms.IntegerField(label='Udo', min_value=20, max_value=300, step_size=1)
#     created_date = forms.DateField(label='Data', input_formats=DATE_INPUT_FORMATS)
#
#     class Meta:
#         model = Reports
#         exclude = ('user',)

