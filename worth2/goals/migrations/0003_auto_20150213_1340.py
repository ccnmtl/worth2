# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import worth2.goals.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0002_goalslotsubmission_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('goal_setting_block', models.ForeignKey(to='goals.GoalSettingBlock', on_delete=models.deletion.CASCADE)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GoalSettingResponse',
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
            name='GoalSettingSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('goal_setting_block', models.ForeignKey(to='goals.GoalSettingBlock', on_delete=models.deletion.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='goalslot',
            name='goal_setting_block',
        ),
        migrations.RemoveField(
            model_name='goalslotoption',
            name='goal_slot',
        ),
        migrations.RemoveField(
            model_name='goalslotresponse',
            name='goal_slot_submission',
        ),
        migrations.RemoveField(
            model_name='goalslotresponse',
            name='option',
        ),
        migrations.DeleteModel(
            name='GoalSlotOption',
        ),
        migrations.DeleteModel(
            name='GoalSlotResponse',
        ),
        migrations.RemoveField(
            model_name='goalslotsubmission',
            name='goal_slot',
        ),
        migrations.DeleteModel(
            name='GoalSlot',
        ),
        migrations.RemoveField(
            model_name='goalslotsubmission',
            name='user',
        ),
        migrations.DeleteModel(
            name='GoalSlotSubmission',
        ),
        migrations.AddField(
            model_name='goalsettingresponse',
            name='goal_setting_submission',
            field=models.ForeignKey(to='goals.GoalSettingSubmission', on_delete=models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goalsettingresponse',
            name='option',
            field=models.ForeignKey(to='goals.GoalOption', on_delete=models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goalsettingblock',
            name='goal_amount',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goalsettingblock',
            name='goal_type',
            field=models.CharField(default=b'services', max_length=255, choices=[(b'services', b'Services'), (b'risk reduction', b'Risk Reduction'), (b'social support', b'Social Support')]),
            preserve_default=True,
        ),
    ]
