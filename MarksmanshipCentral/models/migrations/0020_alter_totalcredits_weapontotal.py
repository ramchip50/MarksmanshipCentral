# Generated by Django 5.0.1 on 2024-03-09 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "0019_alter_session_turnsplayed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="totalcredits",
            name="weapontotal",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
