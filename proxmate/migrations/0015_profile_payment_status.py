# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0014_package_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='payment_status',
            field=models.CharField(default=b'', max_length=128),
        ),
    ]
