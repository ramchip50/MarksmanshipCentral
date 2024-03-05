# Generated by Django 5.0.1 on 2024-02-28 01:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0014_role_remove_person_isstaff_remove_person_issuperuser_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='role',
            new_name='name',
        ),
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='models.role'),
        ),
        migrations.DeleteModel(
            name='PersonRoles',
        ),
    ]