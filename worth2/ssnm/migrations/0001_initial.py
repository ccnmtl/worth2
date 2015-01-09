# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150112_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supporter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('closeness', models.CharField(default=b'VC', max_length=2, choices=[(b'VC', b'Very Close'), (b'C', b'Close'), (b'NC', b'Not Close')])),
                ('influence', models.CharField(default=b'P', max_length=2, choices=[(b'P', b'Positive'), (b'MP', b'Mostly Positive'), (b'MN', b'Mostly Negative'), (b'N', b'Negative')])),
                ('provides_emotional_support', models.BooleanField(default=False)),
                ('provides_practical_support', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('participant', models.ForeignKey(to='main.Participant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
