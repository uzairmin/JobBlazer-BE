# Generated by Django 4.1.5 on 2023-08-25 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead_management', '0006_leadactivitynotesattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]