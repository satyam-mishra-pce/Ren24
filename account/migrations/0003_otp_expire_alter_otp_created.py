# Generated by Django 4.2.7 on 2024-02-23 12:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 23, 12, 13, 42, 769020, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 23, 12, 13, 32, 769020, tzinfo=datetime.timezone.utc)),
        ),
    ]
