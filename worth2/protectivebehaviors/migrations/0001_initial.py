# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProtectiveBehaviorsResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quiz_class', models.CharField(help_text=b'Required', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
