# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20150313_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='avatar',
            name='is_default',
            field=models.BooleanField(default=False, help_text=b'If this is the initial avatar for all participants, set this option to True. There can only be one default avatar in the system.'),
            preserve_default=True,
        ),
    ]
