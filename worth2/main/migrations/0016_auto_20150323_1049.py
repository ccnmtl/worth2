# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_avatar_is_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchedvideo',
            name='video_id',
            field=models.CharField(help_text=b'The youtube video ID', max_length=255, null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='watchedvideo',
            unique_together=set([('user', 'video_id')]),
        ),
        migrations.RemoveField(
            model_name='watchedvideo',
            name='video_block',
        ),
    ]
