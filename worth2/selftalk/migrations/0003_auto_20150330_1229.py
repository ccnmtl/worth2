# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('selftalk', '0002_auto_20150304_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refutationresponse',
            name='refutation',
            field=models.ForeignKey(to='selftalk.Refutation', null=True, on_delete=models.deletion.CASCADE),
            preserve_default=True,
        ),
    ]
