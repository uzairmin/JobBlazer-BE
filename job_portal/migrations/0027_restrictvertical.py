# Generated by Django 4.1.5 on 2023-10-13 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pseudos', '0004_rename_user_team_verticalconfigurations_team'),
        ('job_portal', '0026_jobdetail_tech_stacks'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestrictVertical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_name', models.CharField(max_length=200)),
                ('vertical', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pseudos.verticals')),
            ],
            options={
                'db_table': 'Restrict_Verticals',
                'default_permissions': (),
                'unique_together': {('company_name', 'vertical')},
            },
        ),
    ]
