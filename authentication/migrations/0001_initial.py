# Generated by Django 4.1.5 on 2023-03-03 11:42
import json
import os

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import settings.utils.model_fields.email
import uuid

from settings.base import STATIC_URL


def forwards_func(apps, schema_editor):

    CustomPermission = apps.get_model("authentication", "CustomPermission")
    with open(os.path.join(STATIC_URL, 'permission_files', 'custom_permission.json'), encoding='utf-8') as data_file:
        json_data = json.loads(data_file.read())
        print(json_data)
        for permission_module in json_data:
            module_name = permission_module['module']
            permissions = permission_module['permissions']
            for item in permissions:
                CustomPermission.objects.create(module=module_name, codename=item['codename'], name=item['name'])


def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    CustomPermission = apps.get_model("authentication", "CustomPermission")
    CustomPermission.objects.all().delete()
class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('email', settings.utils.model_fields.email.LowercaseEmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=True)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('code', models.CharField(blank=True, max_length=500, unique=True)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'company',
                'ordering': ['-created_at'],
                'permissions': (('create_company', 'create company'), ('view_company', 'view company'), ('update_company', 'update company'), ('delete_company', 'delete company')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='CustomPermission',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('module', models.CharField(max_length=200)),
                ('codename', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('members', models.ManyToManyField(related_name='reporting_user', to=settings.AUTH_USER_MODEL)),
                ('reporting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'team',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.company')),
                ('permissions', models.ManyToManyField(to='authentication.custompermission')),
            ],
            options={
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
                'db_table': 'role',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reset_code', models.CharField(max_length=10)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reset_password',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PasswordChangeLogs',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'password_change_logs',
            },
        ),
        migrations.CreateModel(
            name='CompanyUser',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_company',
                'ordering': ['-created_at'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='CompanyIntegration',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('api_key', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.company')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ForeignKey(blank=True, help_text='The roles of this user belongs to. A user will get all permissions granted to each of their roles.', null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.role', verbose_name='roles'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_id', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profile',
                'default_permissions': (),
                'unique_together': {('company', 'employee_id')},
            },
        ),
        migrations.RunPython(forwards_func, reverse_func)
    ]
