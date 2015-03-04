# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('selftalk', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refutation',
            name='other_text',
        ),
        migrations.RemoveField(
            model_name='statement',
            name='other_text',
        ),
        migrations.AddField(
            model_name='refutationresponse',
            name='other_text',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='statementresponse',
            name='other_text',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
