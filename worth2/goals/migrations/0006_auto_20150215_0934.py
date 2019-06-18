# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0005_auto_20150213_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalCheckInPageBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GoalCheckInResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('i_will_do_this', models.CharField(max_length=255, choices=[(b'yes', b'Yes'), (b'no', b'No'), (b'in progress', b'In Progress')])),
                ('other', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('goal_setting_response', models.ForeignKey(to='goals.GoalSettingResponse', on_delete=models.deletion.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GoalReviewPageBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='goalsettingblock',
            name='session',
        ),
        migrations.AddField(
            model_name='goalsettingblock',
            name='session_num',
            field=models.PositiveSmallIntegerField(default=1, help_text=b'The session this is associated with (i.e. 1 through 5).'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='goalsettingblock',
            name='goal_amount',
            field=models.PositiveSmallIntegerField(default=1, help_text=b'The number of goals on this block, including the main one.'),
            preserve_default=True,
        ),
    ]
