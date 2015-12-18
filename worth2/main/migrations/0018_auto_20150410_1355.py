# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pagetree', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0017_simpleimageblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_type', models.CharField(default=b'regular', max_length=255, choices=[(b'regular', b'Regular'), (b'makeup', b'Make-Up')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('facilitator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(to='main.Location')),
                ('participant', models.ForeignKey(to='main.Participant')),
                ('section', models.ForeignKey(to='pagetree.Section')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='session',
            name='facilitator',
        ),
        migrations.RemoveField(
            model_name='session',
            name='location',
        ),
        migrations.RemoveField(
            model_name='session',
            name='participant',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
