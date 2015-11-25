# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0004_auto_20151001_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='short_hand',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
