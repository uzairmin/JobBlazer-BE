# Generated by Django 4.1.5 on 2023-06-15 10:32

from django.db import migrations, models

from job_portal.models import AppliedJobStatus, JobDetail


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0008_alter_jobarchive_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jobdetail',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='jobdetail',
            name='job_applied',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='jobdetail',
            unique_together={('company_name', 'job_title', 'job_applied')},
        ),
    ]

