# Generated by Django 3.2.7 on 2021-09-16 07:24

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_battle_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 16, 7, 24, 24, 207756, tzinfo=utc), verbose_name='Время начало'),
        ),
        migrations.AlterField(
            model_name='battlemembers',
            name='battle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.battle', verbose_name='Битва'),
        ),
    ]
