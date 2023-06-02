from django.db import models
from django.contrib.auth.models import AbstractUser

TRAINING = (
    (1, 'Trening pierwszy'),
    (2, 'Trening drugi'),
    (3, 'Trening trzeci'),
    (4, 'Trening czwarty'),
)


class User(AbstractUser):
    """
    User model.
    """
    is_trainer: bool = models.BooleanField(default=False)
    purpose: str = models.TextField()


class MacroElements(models.Model):
    """
    Macro elements model for user.
    """
    calories: int = models.IntegerField()
    protein: int = models.IntegerField()
    fat: int = models.IntegerField()
    carb: int = models.IntegerField()
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)


class Reports(models.Model):
    """
    Report model for creating weekly report with measurements and trainings completed by user.
    """
    MAX_DIGITS: int = 4
    DECIMAL_PLACES: int = 4
    weight: int = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    waist: int = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    stomach: int = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    hip: int = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    thigh: int = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    training_first: bool = models.BooleanField()
    training_second: bool = models.BooleanField()
    training_third: bool = models.BooleanField()
    training_fourth: bool = models.BooleanField()
    comments: str = models.TextField()
    created_date= models.DateField(auto_now_add=True)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_date']


class Photos(models.Model):
    """
    Photos model for creating weekly report by user.
    """
    UPLOAD_FILE: str = 'photos'
    front = models.ImageField(upload_to=UPLOAD_FILE)
    back = models.ImageField(upload_to=UPLOAD_FILE)
    right = models.ImageField(upload_to=UPLOAD_FILE)
    left = models.ImageField(upload_to=UPLOAD_FILE)
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)


class Exercises(models.Model):
    """
    Exercises model for superuser.
    """
    name: str = models.CharField(max_length=255)
    description: str = models.TextField()
    url: str = models.URLField()
    plan = models.ManyToManyField(User, through='PlanExercises')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk']


class PlanExercises(models.Model):
    """
    Model of exercises included in users plan.
    """
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise: Exercises = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    training_number: int = models.IntegerField(TRAINING)
    series: int = models.IntegerField()
    repeat: int = models.IntegerField(null=True)
    TUT: str = models.CharField(max_length=7, null=True)

    class Meta:
        ordering = ['training_number', 'pk']


class PracticalTips(models.Model):
    """
    Practical tips model.
    """
    tip: str = models.TextField()

    class Meta:
        ordering = ['pk']
