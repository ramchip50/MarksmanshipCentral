# Generated by Django 5.0.1 on 2024-03-24 01:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CategoryCredits",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("person_id", models.IntegerField()),
                ("lastname", models.CharField(max_length=50)),
                ("firstname", models.CharField(max_length=50)),
                ("weapon", models.CharField(max_length=50)),
                ("weapon_id", models.IntegerField()),
                ("weaponcredits", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "db_table": "modelview_categorycredits",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Branch",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=125)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Fleet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=125)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("alias", models.CharField(max_length=255)),
                ("verified", models.BooleanField(default=False)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Weapon",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(editable=False, max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name="Award",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("awardname", models.CharField(max_length=25)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="models.branch",
                    ),
                ),
                (
                    "weapon",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="models.weapon",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Chapter",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=125)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "fleet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="models.fleet"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("memberid", models.CharField(max_length=10, unique=True)),
                ("firstname", models.CharField(max_length=50)),
                ("lastname", models.CharField(max_length=50)),
                ("emailaddress", models.CharField(max_length=255)),
                ("passwrd", models.CharField(max_length=50)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="models.branch"
                    ),
                ),
                (
                    "chapter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="models.chapter"
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="models.role",
                    ),
                ),
            ],
            options={
                "verbose_name": "Member",
                "verbose_name_plural": "Members",
            },
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("startdate", models.DateTimeField()),
                ("enddate", models.DateTimeField()),
                ("playmode", models.CharField(max_length=10)),
                ("turnsplayed", models.IntegerField(null=True)),
                ("flagged", models.BooleanField(default=False)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="models.game"
                    ),
                ),
            ],
            options={
                "verbose_name": "Game Session",
                "verbose_name_plural": "Game Sessions",
            },
        ),
        migrations.CreateModel(
            name="NonTRMNParticipants",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fullname", models.CharField(max_length=100, null=True)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="models.session"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SessionParticipants",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("minutes", models.IntegerField()),
                ("credits", models.DecimalField(decimal_places=2, max_digits=10)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="models.person"
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="models.session"
                    ),
                ),
            ],
            options={
                "verbose_name": "Game Session Player",
                "verbose_name_plural": "Game Session Players",
            },
        ),
        migrations.CreateModel(
            name="TotalCredits",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "weapontotal",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("marksman", models.DateField(blank=True, null=True)),
                ("sharpshooter", models.DateField(blank=True, null=True)),
                ("expert", models.DateField(blank=True, null=True)),
                ("high_expert", models.DateField(blank=True, null=True)),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="models.person"
                    ),
                ),
                (
                    "weapon",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="models.weapon",
                    ),
                ),
            ],
            options={
                "verbose_name": "Total Credit Log",
                "verbose_name_plural": "Total Credit Logs",
            },
        ),
        migrations.AddField(
            model_name="game",
            name="weapon",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="models.weapon",
            ),
        ),
        migrations.CreateModel(
            name="AwardSubcategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("createdon", models.DateTimeField(auto_now=True)),
                ("modifiedon", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "award",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="models.award"
                    ),
                ),
                (
                    "weapon",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="models.weapon",
                    ),
                ),
            ],
        ),
    ]
