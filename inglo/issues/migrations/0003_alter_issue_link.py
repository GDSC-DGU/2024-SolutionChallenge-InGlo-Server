# Generated by Django 4.2.6 on 2024-02-19 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_alter_issue_writer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='link',
            field=models.URLField(max_length=500),
        ),
    ]
