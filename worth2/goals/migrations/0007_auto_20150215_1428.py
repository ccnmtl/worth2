# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0006_auto_20150215_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalcheckinpageblock',
            name='session_num',
            field=models.PositiveSmallIntegerField(default=1, help_text=b'The session this is associated with (i.e. 1 through 5).'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goalreviewpageblock',
            name='session_num',
            field=models.PositiveSmallIntegerField(default=1, help_text=b'The session this is associated with (i.e. 1 through 5).'),
            preserve_default=True,
        ),
    ]
