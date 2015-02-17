# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0007_auto_20150215_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalsettingresponse',
            name='form_id',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='goalsettingresponse',
            unique_together=set([('goal_setting_block', 'user', 'form_id')]),
        ),
    ]
