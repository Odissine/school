# Generated by Django 3.2.7 on 2022-05-12 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0009_alter_quiz_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='time_taken',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='time_taken_delta',
        ),
    ]
