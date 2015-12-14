# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoalSettingBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session', models.CharField(max_length=255, choices=[(b'session 1', b'Session 1'), (b'session 2', b'Session 2'), (b'session 3', b'Session 3'), (b'session 4', b'Session 4'), (b'session 5', b'Session 5')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GoalSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('goal_type', models.CharField(max_length=255, choices=[(b'general services', b'General Services'), (b'risk reduction', b'Risk Reduction'), (b'social support', b'Social Support')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('goal_setting_block', models.ForeignKey(to='goals.GoalSettingBlock')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GoalSlotOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('goal_slot', models.ForeignKey(to='goals.GoalSlot')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GoalSlotResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GoalSlotSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('goal_slot', models.ForeignKey(to='goals.GoalSlot')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='goalslotresponse',
            name='goal_slot_submission',
            field=models.ForeignKey(to='goals.GoalSlotSubmission'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goalslotresponse',
            name='option',
            field=models.ForeignKey(to='goals.GoalSlotOption'),
            preserve_default=True,
        ),
    ]
