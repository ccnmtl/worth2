# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_avatarblock'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='session_type',
            field=models.CharField(default=b'regular', max_length=255, choices=[(b'regular', b'Regular'), (b'makeup', b'Make-Up')]),
            preserve_default=True,
        ),
    ]
