# Generated by Django 5.0.1 on 2024-03-25 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "0003_alter_branch_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="session",
            name="flagged",
        ),
        migrations.AddField(
            model_name="session",
            name="dupsessid",
            field=models.IntegerField(null=True),
        ),
    ]