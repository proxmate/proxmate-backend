# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proxmate', '0028_auto_20151116_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('transaction_date', models.DateTimeField(default=datetime.datetime.utcnow, null=True, blank=True)),
                ('payer_email', models.CharField(max_length=256, null=True, blank=True)),
                ('subscription_plan', models.CharField(max_length=64, null=True, blank=True)),
                ('subscription_id', models.CharField(max_length=64, null=True, blank=True)),
                ('supplier', models.CharField(max_length=256, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
