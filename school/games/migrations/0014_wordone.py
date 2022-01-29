# Generated by Django 3.2.7 on 2022-01-24 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('games', '0013_auto_20220124_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordOne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('level', models.IntegerField(default=1)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group')),
            ],
            options={
                'verbose_name': 'Mot',
                'verbose_name_plural': 'Mots',
                'ordering': ('group', 'level', 'name'),
            },
        ),
    ]
