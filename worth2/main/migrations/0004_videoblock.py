# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150112_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_url', models.URLField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
