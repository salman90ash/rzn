# Generated by Django 4.1.7 on 2023-02-26 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TasksData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rzn_number', models.CharField(max_length=255, null=True, verbose_name='Вх. номер')),
                ('rzn_date', models.CharField(max_length=255, null=True, verbose_name='Вх. дата')),
                ('dec_number', models.CharField(max_length=255, null=True, verbose_name='Исх. номер')),
                ('dec_date', models.CharField(max_length=255, null=True, verbose_name='Исх. дата')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('date_UPD', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
            ],
        ),
        migrations.CreateModel(
            name='TasksNotice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Активировать')),
            ],
        ),
        migrations.CreateModel(
            name='TasksType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Активировать')),
            ],
        ),
        migrations.CreateModel(
            name='TasksKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.JSONField(blank=True, default={}, verbose_name='Ключ')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rzn.tasksdata')),
            ],
        ),
        migrations.AddField(
            model_name='tasksdata',
            name='notice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rzn.tasksnotice'),
        ),
        migrations.AddField(
            model_name='tasksdata',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rzn.taskstype'),
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rzn.tasksdata', verbose_name='Сведения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
