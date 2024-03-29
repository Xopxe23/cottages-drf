# Generated by Django 4.2 on 2024-01-22 13:25

import uuid

import django.db.models.deletion
from django.db import migrations, models

import towns.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Населенный пункт',
                'verbose_name_plural': 'Населенные пункты',
            },
        ),
        migrations.CreateModel(
            name='TownImage',
            fields=[
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=towns.models.town_image_path, verbose_name='Фотография')),
                ('town', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='towns.town', verbose_name='Населенный пункт')),
            ],
            options={
                'verbose_name': 'Фотография населенного пункта',
                'verbose_name_plural': 'Фотография населенного пункта',
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TownAttraction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('town', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attractions', to='towns.town', verbose_name='Населенный пункт')),
            ],
            options={
                'verbose_name': 'Достопримечательность',
                'verbose_name_plural': 'Достопримечательности',
            },
        ),
        migrations.CreateModel(
            name='AttractionImage',
            fields=[
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=towns.models.attraction_image_path, verbose_name='Фотография')),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='towns.townattraction', verbose_name='Достопримечательнось')),
            ],
            options={
                'verbose_name': 'Фотография достопримечательности',
                'verbose_name_plural': 'Фотографии достопримечательности',
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]
