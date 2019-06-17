# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0010_auto_20150216_1659'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GoalReviewPageBlock',
        ),
        migrations.RemoveField(
            model_name='goalcheckinpageblock',
            name='session_num',
        ),
        migrations.RemoveField(
            model_name='goalsettingblock',
            name='session_num',
        ),
        migrations.AddField(
            model_name='goalcheckinpageblock',
            name='goal_setting_block',
            field=models.ForeignKey(to='goals.GoalSettingBlock', null=True, on_delete=models.deletion.CASCADE),
            preserve_default=True,
        ),
    ]
