# Generated by Django 5.0 on 2024-02-16 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_customticket_is_paid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='events',
            options={'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
    ]