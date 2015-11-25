# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0007_auto_20151004_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscription_status',
            field=models.CharField(default=b'', max_length=128),
        ),
    ]
