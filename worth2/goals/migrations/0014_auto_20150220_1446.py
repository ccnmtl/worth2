# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0013_auto_20150220_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalcheckinresponse',
            name='what_got_in_the_way',
            field=models.ForeignKey(to='goals.GoalCheckInOption', null=True, on_delete=models.deletion.CASCADE),
            preserve_default=True,
        ),
    ]
