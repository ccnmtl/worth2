# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0011_auto_20150219_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalsettingresponse',
            name='other_text',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
