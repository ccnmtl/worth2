# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0017_auto_20150312_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalcheckinresponse',
            name='goal_setting_response',
            field=models.OneToOneField(related_name='goal_checkin_response', to='goals.GoalSettingResponse'),
        ),
    ]
