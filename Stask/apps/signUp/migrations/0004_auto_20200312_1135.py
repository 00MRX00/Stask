# Generated by Django 3.0.4 on 2020-03-12 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUp', '0003_auto_20200308_2119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userlogpass',
            options={'verbose_name': 'Логин/Пароль', 'verbose_name_plural': 'Логины/Пароли'},
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
