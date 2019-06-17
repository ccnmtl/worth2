# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizblock', '0002_auto_20150202_1707'),
        ('protectivebehaviors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RateMyRiskQuiz',
            fields=[
                ('quiz_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='quizblock.Quiz', on_delete=models.deletion.CASCADE)),
                ('quiz_class', models.CharField(help_text=b'Required', max_length=255)),
            ],
            options={
            },
            bases=('quizblock.quiz',),
        ),
    ]
