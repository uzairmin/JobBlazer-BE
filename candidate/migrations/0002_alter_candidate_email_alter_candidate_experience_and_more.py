# Generated by Django 4.1.5 on 2023-05-25 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='email',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='experience',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='phone',
            field=models.CharField(default='test', max_length=12),
            preserve_default=False,
        ),
    ]
