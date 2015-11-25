# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0023_auto_20151029_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='return_type',
            field=models.CharField(default=b'PROXY', max_length=128, null=True, blank=True),
        ),
    ]
