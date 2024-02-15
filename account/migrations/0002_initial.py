# Generated by Django 5.0 on 2024-02-15 15:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='passes',
            name='Splash',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Splash_Event', to='ticket.events'),
        ),
        migrations.AddField(
            model_name='passes',
            name='technical1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Technical_Event_1', to='ticket.events'),
        ),
        migrations.AddField(
            model_name='passes',
            name='technical2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Technical_Event_2', to='ticket.events'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]