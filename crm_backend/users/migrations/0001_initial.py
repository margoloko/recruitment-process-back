# Generated by Django 4.1 on 2023-08-31 08:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(), users.validators.custom_validate_email])),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество')),
                ('telegram', models.CharField(blank=True, max_length=150, null=True, verbose_name='Telegram')),
                ('role', models.CharField(choices=[('Соискатель', 'Applicant'), ('HR', 'Hr')], default='Соискатель', max_length=11, verbose_name='Роль')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='users/photo/', verbose_name='Фото')),
                ('confirmation_code', models.CharField(default='7687336a-7e3d-4bbf-a912-65f75e895c09', editable=False, max_length=40)),
                ('email_status', models.BooleanField(default=False, verbose_name='Подтверждена почта')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.category', verbose_name='Категория')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['id'],
            },
        ),
    ]
