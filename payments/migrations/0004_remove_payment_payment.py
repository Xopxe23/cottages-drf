# Generated by Django 4.2 on 2024-06-09 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_rename_date_created_payment_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment',
        ),
    ]
