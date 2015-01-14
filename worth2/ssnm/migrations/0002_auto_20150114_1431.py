# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssnm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supporter',
            name='participant',
            field=models.ForeignKey(related_name='supporters', to='main.Participant'),
            preserve_default=True,
        ),
    ]
