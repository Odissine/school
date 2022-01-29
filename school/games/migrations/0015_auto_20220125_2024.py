# Generated by Django 3.2.7 on 2022-01-25 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0014_wordone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ('name',), 'verbose_name': 'Mot (image)', 'verbose_name_plural': 'Mots (image)'},
        ),
        migrations.AlterField(
            model_name='wordone',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
    ]
