# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0009_auto_20151008_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaypalIPNLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('ipn_message', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'User status information',
            },
        ),
    ]
