# Generated by Django 4.1.5 on 2023-05-29 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0003_designation_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='phone',
            field=models.CharField(max_length=30),
        ),
    ]