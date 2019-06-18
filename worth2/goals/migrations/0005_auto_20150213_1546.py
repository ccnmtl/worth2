# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0004_auto_20150213_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goalsettingsubmission',
            name='goal_setting_block',
        ),
        migrations.RemoveField(
            model_name='goalsettingsubmission',
            name='user',
        ),
        migrations.RemoveField(
            model_name='goalsettingresponse',
            name='goal_setting_submission',
        ),
        migrations.DeleteModel(
            name='GoalSettingSubmission',
        ),
        migrations.AddField(
            model_name='goalsettingresponse',
            name='goal_setting_block',
            field=models.ForeignKey(default=None, to='goals.GoalSettingBlock', on_delete=models.deletion.CASCADE),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goalsettingresponse',
            name='user',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE),
            preserve_default=False,
        ),
    ]
