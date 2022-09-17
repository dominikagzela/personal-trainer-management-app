from django.db import models
from django.contrib.auth.models import AbstractUser

TRAINING = (
    (1, 'Trening pierwszy'),
    (2, 'Trening drugi'),
    (3, 'Trening trzeci'),
    (4, 'Trening czwarty'),
)


class User(AbstractUser):
    is_trainer = models.BooleanField(default=False)
    purpose = models.TextField()
    # email = models.EmailField()
    # password = models.CharField()
    # first_name
    # last_name


class MacroElements(models.Model):
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    carb = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Reports(models.Model):
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    waist = models.DecimalField(max_digits=4, decimal_places=1)
    stomach = models.DecimalField(max_digits=4, decimal_places=1)
    hip = models.DecimalField(max_digits=4, decimal_places=1)
    thigh = models.DecimalField(max_digits=4, decimal_places=1)
    training_first = models.BooleanField()
    training_second = models.BooleanField()
    training_third = models.BooleanField()
    training_fourth = models.BooleanField()
    comments = models.TextField()
    created_date = models.DateField(auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_date']


class Photos(models.Model):
    front = models.ImageField(upload_to='photos')
    back = models.ImageField(upload_to='photos')
    right = models.ImageField(upload_to='photos')
    left = models.ImageField(upload_to='photos')
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)


class Exercises(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    plan = models.ManyToManyField(User, through='PlanExercises')

    def __str__(self):
        return self.name


class PlanExercises(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    training_number = models.IntegerField(TRAINING)
    series = models.IntegerField()
    repeat = models.IntegerField(null=True)
    TUT = models.CharField(max_length=7, null=True)

    class Meta:
        ordering = ['training_number', 'pk']


class PracticalTips(models.Model):
    tip = models.TextField()
