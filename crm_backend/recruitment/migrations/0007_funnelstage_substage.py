# Generated by Django 4.1 on 2023-08-22 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recruitment', '0006_alter_vacancy_about_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunnelStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название этапа')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата')),
                ('status', models.CharField(choices=[('1', 'Создан'), ('2', 'Пройден'), ('3', 'Провален')], max_length=5, verbose_name='Статус этапа')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funnel', to=settings.AUTH_USER_MODEL, verbose_name='Кандидат')),
            ],
            options={
                'verbose_name': 'Воронка кандидата',
                'verbose_name_plural': 'Воронки кандидатов',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='SubStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название подэтапа')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата')),
                ('status', models.CharField(choices=[('1', 'Создан'), ('2', 'Пройден'), ('3', 'Провален')], max_length=5, verbose_name='Статус подэтапа')),
                ('stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substage', to='recruitment.funnelstage', verbose_name='Этап воронки')),
            ],
            options={
                'verbose_name': 'Подэтап воронки',
                'verbose_name_plural': 'Подэтапы воронок',
                'ordering': ['-date'],
            },
        ),
    ]
