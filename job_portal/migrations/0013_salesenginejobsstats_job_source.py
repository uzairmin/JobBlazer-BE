# Generated by Django 4.1.5 on 2023-06-23 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0012_jobdetail_estimated_salary_jobdetail_expired_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesenginejobsstats',
            name='job_source',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
