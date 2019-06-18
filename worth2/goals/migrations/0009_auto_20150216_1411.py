# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0008_auto_20150216_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalCheckInOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('text', models.TextField(help_text=b'An option for the "What got in the way" dropdown for goal check-in.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='goalcheckinresponse',
            name='what_got_in_the_way',
            field=models.ForeignKey(default=None, to='goals.GoalOption', on_delete=models.deletion.CASCADE),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goalcheckinresponse',
            name='goal_setting_response',
            field=models.ForeignKey(to='goals.GoalSettingResponse', unique=True, on_delete=models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='goaloption',
            name='text',
            field=models.TextField(help_text=b'An option for the dropdowns in a specific GoalSetting pageblock.'),
            preserve_default=True,
        ),
    ]
