# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Refutation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('text', models.TextField()),
                ('other_text', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RefutationBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RefutationResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('refutation', models.ForeignKey(to='selftalk.Refutation')),
                ('refutation_block', models.ForeignKey(to='selftalk.RefutationBlock')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('text', models.TextField()),
                ('other_text', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatementBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_internal', models.BooleanField(default=True, help_text=b'If True, this will be rendered as a "My Self Talk" block. Otherwise this block\'s subject is a video.')),
                ('subject_name', models.TextField(help_text=b'(optional) The name of the video subject for this block, e.g. "Jane"', null=True, blank=True)),
                ('statements', models.ManyToManyField(to='selftalk.Statement')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatementResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('statement', models.ForeignKey(to='selftalk.Statement')),
                ('statement_block', models.ForeignKey(to='selftalk.StatementBlock')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='statementresponse',
            unique_together=set([('statement', 'statement_block', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='refutationresponse',
            unique_together=set([('refutation', 'refutation_block', 'user')]),
        ),
        migrations.AddField(
            model_name='refutationblock',
            name='statement_block',
            field=models.ForeignKey(to='selftalk.StatementBlock'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='refutation',
            name='statement',
            field=models.ForeignKey(to='selftalk.Statement'),
            preserve_default=True,
        ),
    ]
