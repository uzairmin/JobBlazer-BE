# Generated by Django 4.1.5 on 2023-10-31 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0028_salesenginejobsstats_source_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesenginejobsstats',
            name='jobs_count',
            field=models.IntegerField(default=0),
        ),
    ]
