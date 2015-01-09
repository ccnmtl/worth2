# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_participant_cohort_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='cohort_id',
            field=models.CharField(blank=True, max_length=255, null=True, db_index=True, validators=[django.core.validators.RegexValidator(regex=b'\\d{3}', message=b"That cohort ID isn't valid")]),
            preserve_default=True,
        ),
    ]
