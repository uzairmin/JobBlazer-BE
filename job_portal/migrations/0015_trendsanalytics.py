# Generated by Django 3.2.20 on 2023-08-11 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0014_jobdetail_job_description_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrendsAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.CharField(max_length=50, unique=True)),
                ('tech_stacks', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
