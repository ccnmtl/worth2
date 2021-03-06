# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-11 16:30
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20170424_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='study_id',
            field=models.CharField(
                db_index=True,
                max_length=255,
                unique=True,
                validators=[django.core.validators.RegexValidator(
                    message=b"That study ID isn't valid. The format " +
                    b"is: RRHHMMDDMMYBS",
                    regex=b'^\\d\\d[0-2]\\d[0-5]\\d[0-3]\\d[0-1]' +
                    b'\\d[5-9][1-5][1-2]$'
                )]),
        ),
    ]
