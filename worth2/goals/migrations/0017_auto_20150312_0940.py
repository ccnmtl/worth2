# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0016_auto_20150227_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goaloption',
            name='goal_setting_block',
        ),
        migrations.AddField(
            model_name='goaloption',
            name='goal_type',
            field=models.CharField(default=b'services', max_length=255, db_index=True, choices=[(b'services', b'Services'), (b'risk reduction', b'Risk Reduction'), (b'social support', b'Social Support')]),
            preserve_default=True,
        ),
    ]
