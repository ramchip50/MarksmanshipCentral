# Generated by Django 5.0.1 on 2024-03-24 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("models", "0001_initial"),
    ]

    operations = [
         migrations.DeleteModel(
            name="Award",
        ),
        migrations.DeleteModel(
            name="AwardSubcategory",
        ),
    ]
