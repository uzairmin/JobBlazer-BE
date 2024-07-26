# Generated by Django 3.2.19 on 2023-08-24 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lead_management', '0005_lead_converter'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadActivityNotesAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('attachment', models.TextField(blank=True, null=True)),
                ('filename', models.CharField(blank=True, max_length=256)),
                ('lead_activity_notes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lead_management.leadactivitynotes')),
            ],
            options={
                'db_table': 'lead_activity_notes_attachments',
                'default_permissions': (),
            },
        ),
    ]