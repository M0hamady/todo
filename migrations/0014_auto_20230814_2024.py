# Generated by Django 3.2.19 on 2023-08-14 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0013_auto_20230814_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskfeedback',
            name='sprints',
        ),
        migrations.AddField(
            model_name='task',
            name='sprints',
            field=models.ManyToManyField(related_name='tasks_sprints', to='todo.Sprint'),
        ),
    ]
