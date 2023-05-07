from django import forms
from betterforms.multiform import MultiModelForm
from .models import (
    MacroElements,
    Reports, Photos,
    Exercises,
    PlanExercises,
    PracticalTips,
)


class LoginUserForm(forms.Form):
    """
    Login form.
    """
    username = forms.CharField(label='Login', max_length=265)
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class PracticalTipForm(forms.ModelForm):
    """
    Practical tip form for superuser.
    """
    class Meta:
        model = PracticalTips
        fields = ['tip']
        labels = {'tip': 'Opis'}


class MacroElementsForm(forms.ModelForm):
    """
    Macro elements form for superuser.
    """
    STEP_SIZE = 1
    calories = forms.IntegerField(label='Kalorie (kcal)', min_value=1000, max_value=8000, step_size=STEP_SIZE)
    protein = forms.IntegerField(label='Białko (g)', min_value=1, max_value=800, step_size=STEP_SIZE)
    fat = forms.IntegerField(label='Tłuszcze (g)', min_value=1, max_value=800, step_size=STEP_SIZE)
    carb = forms.IntegerField(label='Węglowodany (g)', min_value=1, max_value=1500, step_size=STEP_SIZE)

    class Meta:
        model = MacroElements
        exclude = ['user']


class ExercisesForm(forms.ModelForm):
    """
    Exercises form for superuser.
    """
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
    """
    Form for plan of exercises for superuser.
    """
    STEP_SIZE = 1
    MIN_VALUE = 1
    exercise = forms.ModelChoiceField(queryset=Exercises.objects.all(), label='Ćwiczenie',
                                      empty_label=None, to_field_name='name')
    series = forms.IntegerField(label='Serie', min_value=MIN_VALUE, max_value=10, step_size=STEP_SIZE)
    repeat = forms.IntegerField(label='Powtórzenia', min_value=MIN_VALUE, max_value=50, step_size=STEP_SIZE)

    class Meta:
        model = PlanExercises
        fields = [
            'exercise',
            'series',
            'repeat',
            'TUT',
        ]


class ReportForm(forms.ModelForm):
    """
    Report form for client.
    """
    MIN_VALUE = 20
    MAX_VALUE = 300
    STEP_SIZE = 1
    weight = forms.IntegerField(label='Waga (kg)', min_value=MIN_VALUE, max_value=MAX_VALUE, step_size=STEP_SIZE)
    waist = forms.IntegerField(label='Talia (cm)', min_value=MIN_VALUE, max_value=MAX_VALUE, step_size=STEP_SIZE)
    stomach = forms.IntegerField(label='Brzuch (cm)', min_value=MIN_VALUE, max_value=MAX_VALUE, step_size=STEP_SIZE)
    hip = forms.IntegerField(label='Biodra (cm)', min_value=MIN_VALUE, max_value=MAX_VALUE, step_size=STEP_SIZE)
    thigh = forms.IntegerField(label='Udo (cm)', min_value=MIN_VALUE, max_value=MAX_VALUE, step_size=STEP_SIZE)
    training_first = forms.BooleanField(label='Trening 1', required=False)
    training_second = forms.BooleanField(label='Trening 2', required=False)
    training_third = forms.BooleanField(label='Trening 3', required=False)
    training_fourth = forms.BooleanField(label='Trening 4', required=False)
    comments = forms.CharField(widget=forms.Textarea, label='Komentarz')

    class Meta:
        model = Reports
        exclude = ['user', 'created_date']


class PhotosForm(forms.ModelForm):
    """
    Photos form for creating report by client.
    """
    class Meta:
        model = Photos
        exclude = ['report']
        labels = {
            'front': 'Przód',
            'back': 'Tył',
            'right': 'Prawa strona',
            'left': 'Lewa strona',
        }


class ReportPhotosMultiForm(MultiModelForm):
    """
    Report and photos form combined.
    """
    form_classes = {
        'report': ReportForm,
        'photos': PhotosForm,
    }
