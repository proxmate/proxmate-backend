# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0024_auto_20151029_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='transaction_date',
            field=models.DateTimeField(default=datetime.datetime.utcnow, null=True, blank=True),
        ),
    ]
