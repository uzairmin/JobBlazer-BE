# Generated by Django 3.2.20 on 2023-08-15 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0015_trendsanalytics'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='jobarchive',
            name='job_archive_company_0e85ea_idx',
        ),
        migrations.AddIndex(
            model_name='jobarchive',
            index=models.Index(fields=['job_source', 'tech_keywords', 'job_posted_date', 'created_at'], name='job_archive_job_sou_50203f_idx'),
        ),
    ]