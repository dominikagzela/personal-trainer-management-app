# Generated by Django 4.1.1 on 2022-09-08 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0005_exercises_planexercises_exercises_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='surname',
        ),
    ]
