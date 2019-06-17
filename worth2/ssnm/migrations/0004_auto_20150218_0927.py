# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ssnm', '0003_ssnmpageblock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supporter',
            name='participant',
        ),
        migrations.AddField(
            model_name='supporter',
            name='user',
            field=models.ForeignKey(related_name='supporters', to=settings.AUTH_USER_MODEL, null=True, on_delete=models.deletion.CASCADE),
            preserve_default=True,
        ),
    ]
