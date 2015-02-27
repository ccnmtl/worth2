# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0014_auto_20150220_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalsettingresponse',
            name='goal_setting_block',
            field=models.ForeignKey(related_name='goal_setting_responses', to='goals.GoalSettingBlock'),
            preserve_default=True,
        ),
    ]
