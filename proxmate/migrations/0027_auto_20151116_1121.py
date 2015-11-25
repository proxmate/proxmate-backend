# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0026_auto_20151113_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='is_closable',
            field=models.BooleanField(default=False),
        ),
    ]
