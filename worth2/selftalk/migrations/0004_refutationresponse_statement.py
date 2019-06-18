# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('selftalk', '0003_auto_20150330_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='refutationresponse',
            name='statement',
            field=models.ForeignKey(to='selftalk.Statement', null=True, on_delete=models.deletion.CASCADE),
            preserve_default=True,
        ),
    ]
