# Generated by Django 3.2.19 on 2023-11-21 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0029_company_slack_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='slack_channel',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
