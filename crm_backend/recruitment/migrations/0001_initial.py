# Generated by Django 4.1 on 2023-08-31 08:33

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import recruitment.utils
import users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantResume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100, verbose_name='Должность')),
                ('employment_type', multiselectfield.db.fields.MultiSelectField(choices=[('PO', 'Полная'), ('CH', 'Частичная'), ('PR', 'Проектная'), ('ST', 'Стажировка')], default=['PO'], max_length=11, verbose_name='Тип занятости')),
                ('schedule_work', multiselectfield.db.fields.MultiSelectField(choices=[('P', 'Офис'), ('G', 'Гибрид'), ('U', 'Удаленный'), ('W', 'Вахтовый')], default=['P'], max_length=7, verbose_name='Расписание работы')),
                ('salary_expectations', models.CharField(default='з/п не указана', max_length=50, verbose_name='Желаемая зарплата')),
                ('working_trip', models.BooleanField(blank=True, null=True, verbose_name='Командировка')),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('education', models.CharField(choices=[('SR', 'Среднее'), ('VN', 'Высшее неполное'), ('VS', 'Высшее'), ('RC', 'Переподготовка')], max_length=2, verbose_name='Образование')),
                ('town', models.CharField(max_length=50, null=True, verbose_name='Город проживания')),
                ('citizenship', models.CharField(max_length=50, null=True, verbose_name='Гражданство')),
                ('bday', models.DateField(verbose_name='Дата рождения')),
                ('about_me', models.TextField(max_length=700, verbose_name='Коротко о себе')),
                ('current_company', models.CharField(blank=True, max_length=50, null=True, verbose_name='Текущее место работы')),
                ('current_job', models.CharField(blank=True, max_length=50, null=True, verbose_name='Текущяя должность')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации резюме')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_resumes', to=settings.AUTH_USER_MODEL, verbose_name='Соискатель')),
            ],
            options={
                'verbose_name': 'Резюме',
                'verbose_name_plural': 'Резюме',
                'ordering': ['job_title'],
            },
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество')),
                ('bday', models.DateField(verbose_name='Дата рождения')),
                ('city', models.CharField(max_length=50, verbose_name='Город проживания')),
                ('last_job', models.CharField(max_length=90, verbose_name='Последнее место работы')),
                ('cur_position', models.CharField(max_length=50, null=True, verbose_name='Текущая должность')),
                ('salary_expectations', models.CharField(default='з/п не указана', max_length=50, verbose_name='Желаемая зарплата')),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(), users.validators.custom_validate_email], verbose_name='Почта')),
                ('telegram', models.CharField(blank=True, max_length=150, null=True, verbose_name='Телеграмм')),
                ('portfolio', models.URLField(null=True, verbose_name='Ссылка на портфолио')),
                ('resume', models.FileField(upload_to='candidates/resumes', verbose_name='Резюме')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_title', models.CharField(max_length=100, verbose_name='Название компании')),
                ('about_company', models.TextField(help_text='Введите информацию о компани', null=True, verbose_name='О компании')),
                ('company_address', models.CharField(max_length=100, null=True, verbose_name='Адрес компании')),
                ('website', models.URLField(max_length=120, verbose_name='Сайт компании')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Эл.почта')),
                ('phone_number', models.CharField(max_length=16, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('link_hr', models.URLField(max_length=100, null=True, verbose_name='Ссылка на HR')),
                ('logo', models.ImageField(null=True, upload_to=recruitment.utils.generate_logo_path, verbose_name='Логотип компании')),
            ],
            options={
                'verbose_name': 'Основная информация о компании',
                'verbose_name_plural': 'Основная информация о компании',
                'ordering': ['company_title'],
            },
        ),
        migrations.CreateModel(
            name='FunnelStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название этапа')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата')),
                ('status', models.CharField(choices=[('1', 'Создан'), ('2', 'Пройден'), ('3', 'Провален')], default='1', max_length=5, verbose_name='Статус этапа')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funnel', to='recruitment.candidate', verbose_name='Кандидат')),
            ],
            options={
                'verbose_name': 'Воронка кандидата',
                'verbose_name_plural': 'Воронки кандидатов',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Дата начала работы')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Дата увольнения')),
                ('position', models.CharField(max_length=50, verbose_name='Должность')),
                ('organization', models.CharField(max_length=50, verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Опыт работы',
                'verbose_name_plural': 'Опыт работы',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacancy_title', models.CharField(max_length=100, verbose_name='Название вакансии')),
                ('required_experience', models.CharField(choices=[('1', 'Без опыта'), ('2', '1-3 года'), ('3', '3-5 лет'), ('4', 'Более 5 лет')], max_length=1, null=True, verbose_name='Требуемый опыт работы')),
                ('employment_type', multiselectfield.db.fields.MultiSelectField(choices=[('PO', 'Полная'), ('CH', 'Частичная'), ('PR', 'Проектная'), ('ST', 'Стажировка')], max_length=11, null=True, verbose_name='Тип занятости')),
                ('schedule_work', multiselectfield.db.fields.MultiSelectField(choices=[('P', 'Офис'), ('G', 'Гибрид'), ('U', 'Удаленный'), ('W', 'Вахтовый')], max_length=7, null=True, verbose_name='Расписание работы')),
                ('education', multiselectfield.db.fields.MultiSelectField(choices=[('SR', 'Среднее'), ('VN', 'Высшее неполное'), ('VS', 'Высшее'), ('RC', 'Переподготовка')], max_length=11, null=True, verbose_name='Образование')),
                ('salary', models.CharField(default='з/п не указана', max_length=50, verbose_name='Заработная плата')),
                ('about_company', models.TextField(blank=True, help_text='Введите информацию о компани', null=True, verbose_name='О компании')),
                ('city', models.CharField(max_length=30, verbose_name='Город')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации вакансии')),
                ('job_conditions', models.TextField(help_text='Введите условия работы', verbose_name='Условия работы')),
                ('job_responsibilities', models.TextField(help_text='Введите обязанности кандидата', verbose_name='Обязанности кандидата')),
                ('technology_stack', models.TextField(verbose_name='Ключевые навыки')),
                ('status', models.CharField(choices=[('A', 'activeVacancies'), ('F', 'completedVacancies'), ('D', 'draftVacancies')], default='D', max_length=1, verbose_name='Статус вакансии')),
                ('deadline', models.DateField(default=datetime.date(2023, 9, 30), verbose_name='Срок закрытия вакансии')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='recruitment.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Основная информация о вакансии',
                'verbose_name_plural': 'Основная информация о вакансии',
                'ordering': ['pub_date'],
            },
        ),
        migrations.CreateModel(
            name='SubStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название подэтапа')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата')),
                ('status', models.CharField(choices=[('1', 'Создан'), ('2', 'Пройден'), ('3', 'Провален')], default='1', max_length=5, verbose_name='Статус подэтапа')),
                ('stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substage', to='recruitment.funnelstage', verbose_name='Этап воронки')),
            ],
            options={
                'verbose_name': 'Подэтап воронки',
                'verbose_name_plural': 'Подэтапы воронок',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Заметка', verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notes', to=settings.AUTH_USER_MODEL)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.candidate', verbose_name='Кандидат')),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('conference_link', models.URLField(blank=True, max_length=255, null=True)),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidate_events', to='recruitment.candidate')),
                ('hr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('educational_institution', models.CharField(max_length=250, verbose_name='Учебное заведение')),
                ('faculty', models.CharField(max_length=100, verbose_name='Факультет')),
                ('specialization', models.CharField(max_length=100, verbose_name='Специальность')),
                ('graduation', models.DateField(blank=True, null=True, verbose_name='Год окончания')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='recruitment.applicantresume', verbose_name='резюме')),
            ],
            options={
                'verbose_name': 'Информация об образовавании',
                'verbose_name_plural': 'Информация об образовавании',
                'ordering': ['graduation'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Комментарий', verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='recruitment.note')),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.AddField(
            model_name='candidate',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='recruitment.vacancy', verbose_name='Вакансия'),
        ),
        migrations.AddField(
            model_name='applicantresume',
            name='work_experiences',
            field=models.ManyToManyField(to='recruitment.workexperience', verbose_name='Информация об опыте работы'),
        ),
    ]
