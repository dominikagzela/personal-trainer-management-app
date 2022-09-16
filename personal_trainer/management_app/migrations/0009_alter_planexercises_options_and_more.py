# Generated by Django 4.1.1 on 2022-09-16 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0008_alter_planexercises_tut'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='planexercises',
            options={'ordering': ['training_number', 'pk']},
        ),
        migrations.AlterField(
            model_name='planexercises',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_app.exercises', verbose_name='Ćwiczenie'),
        ),
    ]