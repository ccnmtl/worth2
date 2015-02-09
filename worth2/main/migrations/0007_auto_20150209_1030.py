# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150206_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protectivebehaviorresults',
            name='quiz_class',
            field=models.CharField(help_text=b'Required', max_length=255),
            preserve_default=True,
        ),
    ]
