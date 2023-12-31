# Generated by Django 3.2.19 on 2023-08-17 19:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0018_project_roadmapitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='roadmapitem',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
