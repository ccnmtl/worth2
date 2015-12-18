# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0012_goalsettingresponse_other_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalcheckinresponse',
            name='i_will_do_this',
            field=models.CharField(max_length=255, choices=[(b'yes', b'I did it!'), (b'in progress', b"I'm still working on it."), (b'no', b"I haven't started this goal.")]),
            preserve_default=True,
        ),
    ]
