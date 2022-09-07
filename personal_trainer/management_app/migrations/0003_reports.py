# Generated by Django 4.1.1 on 2022-09-07 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0002_macroelements'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_created=True)),
                ('weight', models.DecimalField(decimal_places=1, max_digits=4)),
                ('waist', models.DecimalField(decimal_places=1, max_digits=4)),
                ('stomach', models.DecimalField(decimal_places=1, max_digits=4)),
                ('hip', models.DecimalField(decimal_places=1, max_digits=4)),
                ('thigh', models.DecimalField(decimal_places=1, max_digits=4)),
                ('training_first', models.BooleanField()),
                ('training_second', models.BooleanField()),
                ('training_third', models.BooleanField()),
                ('training_fourth', models.BooleanField()),
                ('comments', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
