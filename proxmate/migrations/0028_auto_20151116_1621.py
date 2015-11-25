# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0027_auto_20151116_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_active_check',
            field=models.CharField(default=b'', max_length=128),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_channel_check',
            field=models.CharField(default=b'', max_length=128),
        ),
    ]
