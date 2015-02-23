# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizblock', '0003_auto_20150209_1601'),
        ('protectivebehaviors', '0002_ratemyriskquiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratemyriskquiz',
            name='quiz_ptr',
        ),
        migrations.DeleteModel(
            name='RateMyRiskQuiz',
        ),
        migrations.AlterField(
            model_name='protectivebehaviorsresults',
            name='quiz_class',
            field=models.CharField(default=b'protective-behaviors', help_text=b'Required', max_length=255),
            preserve_default=True,
        ),
    ]
