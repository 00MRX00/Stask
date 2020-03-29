# Generated by Django 3.0.4 on 2020-03-27 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUp', '0004_auto_20200312_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_title', models.CharField(max_length=255, verbose_name='Название проекта')),
                ('project_description', models.TextField(max_length=3000, verbose_name='Описание проекта')),
                ('project_creation_date', models.DateTimeField(verbose_name='Дата создания проекта')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
    ]