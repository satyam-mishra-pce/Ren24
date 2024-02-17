# Generated by Django 5.0 on 2024-02-16 05:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user__pass_alter_passes_splash_and_more'),
        ('ticket', '0002_events_includedinpass_alter_events_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passes',
            name='Splash',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Splash_Event', to='ticket.events'),
        ),
        migrations.AlterField(
            model_name='passes',
            name='technical1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Technical_Event_1', to='ticket.events'),
        ),
        migrations.AlterField(
            model_name='passes',
            name='technical2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Technical_Event_2', to='ticket.events'),
        ),
    ]