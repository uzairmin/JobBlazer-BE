# Generated by Django 4.1.5 on 2023-05-22 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_alter_custompermission_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='custompermission',
            name='level',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]