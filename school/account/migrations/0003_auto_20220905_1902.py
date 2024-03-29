# Generated by Django 3.2.7 on 2022-09-05 19:02

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('account', '0002_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2022, 9, 5, 19, 2, 5, 41209, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='prev_group',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, related_name='Players', to='auth.group'),
        ),
    ]
