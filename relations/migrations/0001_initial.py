# Generated by Django 4.2 on 2024-01-07 21:09

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cottages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCottageReview',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cottage_rating', models.IntegerField(choices=[(1, 'Очень плохо'), (2, 'Плохо'), (3, 'Нормально'), (4, 'Хорошо'), (5, 'Отлично')])),
                ('cleanliness_rating', models.IntegerField(choices=[(1, 'Очень плохо'), (2, 'Плохо'), (3, 'Нормально'), (4, 'Хорошо'), (5, 'Отлично')])),
                ('owner_rating', models.IntegerField(choices=[(1, 'Очень плохо'), (2, 'Плохо'), (3, 'Нормально'), (4, 'Хорошо'), (5, 'Отлично')])),
                ('comment', models.TextField()),
                ('cottage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='cottages.cottage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCottageRent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('cottage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents', to='cottages.cottage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCottageLike',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cottage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='cottages.cottage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
