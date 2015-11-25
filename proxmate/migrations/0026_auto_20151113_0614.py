# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0025_auto_20151103_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='is_persistent',
        ),
        migrations.AddField(
            model_name='message',
            name='is_closable',
            field=models.BooleanField(default=True),
        ),
    ]
