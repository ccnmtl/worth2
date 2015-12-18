# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_videoblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProtectiveBehaviorResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quiz_class', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
