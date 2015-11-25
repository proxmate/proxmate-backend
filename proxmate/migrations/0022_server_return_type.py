# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0021_delete_reports'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='return_type',
            field=models.BooleanField(default=True),
        ),
    ]
