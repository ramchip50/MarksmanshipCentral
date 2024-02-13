# Generated by Django 5.0.1 on 2024-02-13 03:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalCredits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weaponsubcategory', models.CharField(max_length=25)),
                ('weapontotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.person')),
            ],
        ),
    ]
