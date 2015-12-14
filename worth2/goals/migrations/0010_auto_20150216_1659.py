# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0009_auto_20150216_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalcheckinresponse',
            name='what_got_in_the_way',
            field=models.ForeignKey(to='goals.GoalCheckInOption'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='goalsettingblock',
            name='session_num',
            field=models.PositiveSmallIntegerField(default=1, help_text=b'The session this is associated with (i.e. 1 through 5).', db_index=True),
            preserve_default=True,
        ),
    ]
