# Generated by Django 3.2.19 on 2023-08-20 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0023_auto_20230819_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duration',
            name='duration',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
