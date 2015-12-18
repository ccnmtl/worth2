# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20150225_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='study_id',
            field=models.CharField(db_index=True, unique=True, max_length=255, validators=[django.core.validators.RegexValidator(regex=b'^\\d{12}$', message=b"That study ID isn't valid. (It needs to be 12 digits)")]),
            preserve_default=True,
        ),
    ]
