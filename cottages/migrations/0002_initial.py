# Generated by Django 4.2 on 2024-01-19 16:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('towns', '0001_initial'),
        ('cottages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cottage',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='cottage',
            name='town',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='towns.town', verbose_name='Населенный пункт'),
        ),
    ]
