# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150209_1030'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProtectiveBehaviorResults',
        ),
    ]
