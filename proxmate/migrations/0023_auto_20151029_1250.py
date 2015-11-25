# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0022_server_return_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='return_type',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
