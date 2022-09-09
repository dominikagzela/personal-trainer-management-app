# Generated by Django 4.1.1 on 2022-09-07 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0003_reports'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('front', models.ImageField(upload_to='photos')),
                ('back', models.ImageField(upload_to='photos')),
                ('right', models.ImageField(upload_to='photos')),
                ('left', models.ImageField(upload_to='photos')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_app.reports')),
            ],
        ),
    ]