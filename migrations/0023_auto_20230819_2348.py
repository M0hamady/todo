# Generated by Django 3.2.19 on 2023-08-19 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0022_auto_20230819_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='duration',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='duration',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
