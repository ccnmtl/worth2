# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_videoblock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoblock',
            name='video_url',
        ),
        migrations.AddField(
            model_name='videoblock',
            name='video_height',
            field=models.PositiveSmallIntegerField(default=315),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='videoblock',
            name='video_mp4_url',
            field=models.URLField(help_text=b'An mp4 is required to play the video on iOS.', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='videoblock',
            name='video_ogg_url',
            field=models.URLField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='videoblock',
            name='video_webm_url',
            field=models.URLField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='videoblock',
            name='video_width',
            field=models.PositiveSmallIntegerField(default=560),
            preserve_default=True,
        ),
    ]
