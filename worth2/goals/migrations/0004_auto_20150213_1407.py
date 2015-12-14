# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import worth2.goals.models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_auto_20150213_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalsettingblock',
            name='goal_amount',
            field=models.PositiveSmallIntegerField(default=1, help_text=b'The number of goals on this block, including the main one.'),
            preserve_default=True,
        ),
    ]
