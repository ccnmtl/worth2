# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_protectivebehaviorresults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protectivebehaviorresults',
            name='quiz_class',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
