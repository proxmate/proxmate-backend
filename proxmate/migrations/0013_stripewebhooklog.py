# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0012_auto_20151008_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeWebhookLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('webhook_message', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'User status information',
            },
        ),
    ]
