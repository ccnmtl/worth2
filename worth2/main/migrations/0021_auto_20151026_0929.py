# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import worth2.main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20151016_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='study_id',
            field=models.CharField(db_index=True, unique=True, max_length=255, validators=[django.core.validators.RegexValidator(regex=b'^[1-2]\\d[0-1]\\d[0-3]\\d\\d\\d[0-2]\\d[0-5]\\d$', message=b"That study ID isn't valid. The format is: YYMMDDLLHHMM (where LL is the two-digit location code)."), worth2.main.models.study_id_validator]),
        ),
    ]
