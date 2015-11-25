# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0017_auto_20151018_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_updated_user',
            field=models.BooleanField(default=False),
        ),
    ]
