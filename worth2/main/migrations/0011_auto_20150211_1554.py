# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_session_session_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvatarSelectorBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='participant',
            name='cohort_id',
            field=models.CharField(blank=True, max_length=255, null=True, db_index=True, validators=[django.core.validators.RegexValidator(regex=b'^\\d{3}$', message=b"That cohort ID isn't valid. (It needs to be 3 digits)")]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participant',
            name='study_id',
            field=models.CharField(db_index=True, unique=True, max_length=255, validators=[django.core.validators.RegexValidator(regex=b'^7.*$', message=b"That study ID isn't valid. (It needs to start with a 7)")]),
            preserve_default=True,
        ),
    ]
