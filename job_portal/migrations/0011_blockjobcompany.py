# Generated by Django 4.1.5 on 2023-06-20 15:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_custompermission_options'),
        ('job_portal', '0010_alter_jobdetail_job_applied'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockJobCompany',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.company')),
            ],
            options={
                'default_permissions': (),
            },
        ),
    ]