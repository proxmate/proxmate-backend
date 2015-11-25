# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0006_auto_20151004_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_generic',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='message',
            name='specific_to_plan',
            field=models.CharField(max_length=256, blank=True),
        ),
    ]
