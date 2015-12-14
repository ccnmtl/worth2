# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20150211_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoblock',
            name='video_url',
        ),
        migrations.AddField(
            model_name='videoblock',
            name='video_id',
            field=models.CharField(help_text=b'The YouTube video id, e.g. "M7lc1UVf-VE"', max_length=255, null=True),
            preserve_default=True,
        ),
    ]
