# Generated by Django 2.2.6 on 2020-05-24 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_job_position'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Job_Position',
            new_name='JobPosition',
        ),
    ]
