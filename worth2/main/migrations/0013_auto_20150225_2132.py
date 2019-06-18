# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0012_auto_20150224_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchedVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='watched_videos', to=settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE)),
                ('video_block', models.ForeignKey(to='main.VideoBlock', on_delete=models.deletion.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='watchedvideo',
            unique_together=set([('user', 'video_block')]),
        ),
    ]
