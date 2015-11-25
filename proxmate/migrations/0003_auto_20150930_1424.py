# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0002_auto_20150928_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='plan_status',
            field=models.CharField(default=b'no_plan', max_length=128),
        ),
        migrations.AlterField(
            model_name='package',
            name='allow_multiple_countries',
            field=models.BooleanField(default=False),
        ),
    ]
