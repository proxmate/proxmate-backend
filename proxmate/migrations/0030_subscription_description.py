# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0029_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='description',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
