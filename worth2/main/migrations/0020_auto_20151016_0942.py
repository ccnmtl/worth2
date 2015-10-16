# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20150701_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='study_id',
            field=models.CharField(unique=True, max_length=255, db_index=True),
        ),
    ]
