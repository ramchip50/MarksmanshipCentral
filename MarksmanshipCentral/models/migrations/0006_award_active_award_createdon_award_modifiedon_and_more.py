# Generated by Django 5.0.1 on 2024-02-15 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0005_award_awardsubcategory_nontrmnparticipants_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='award',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='award',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='awardsubcategory',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='awardsubcategory',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='awardsubcategory',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='fleet',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='fleet',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='fleet',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='game',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='game',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='game',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='nontrmnparticipants',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='nontrmnparticipants',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='nontrmnparticipants',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='peopleawards',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='peopleawards',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='peopleawards',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='person',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='person',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='person',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='session',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='session',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='session',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='sessionparticipants',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sessionparticipants',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='sessionparticipants',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='totalcredits',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='totalcredits',
            name='createdon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='totalcredits',
            name='modifiedon',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='session',
            name='flagged',
            field=models.BooleanField(default=False),
        ),
    ]