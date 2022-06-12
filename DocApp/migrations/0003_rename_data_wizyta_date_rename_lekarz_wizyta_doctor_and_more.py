# Generated by Django 4.0.4 on 2022-05-29 11:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('DocApp', '0002_remove_wizyta_czy_nfz'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wizyta',
            old_name='data',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='wizyta',
            old_name='lekarz',
            new_name='doctor',
        ),
        migrations.RenameField(
            model_name='wizyta',
            old_name='pacjent',
            new_name='user',
        ),
        migrations.AddField(
            model_name='wizyta',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
