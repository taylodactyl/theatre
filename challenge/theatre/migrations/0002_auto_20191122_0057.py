# Generated by Django 2.2.7 on 2019-11-22 00:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theatre', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='showing',
            new_name='screening',
        ),
        migrations.AddField(
            model_name='ticket',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 11, 22, 0, 57, 35, 55402)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.PositiveIntegerField(default=100),
        ),
    ]