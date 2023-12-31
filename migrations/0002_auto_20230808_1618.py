# Generated by Django 3.2.19 on 2023-08-08 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('admin_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.admincompany')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.admincompany')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('memo', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('duration', models.PositiveIntegerField()),
                ('week_of_month', models.PositiveIntegerField()),
                ('assigned_to', models.ManyToManyField(blank=True, to='todo.Employee')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.company')),
            ],
        ),
        migrations.DeleteModel(
            name='Todo',
        ),
    ]
