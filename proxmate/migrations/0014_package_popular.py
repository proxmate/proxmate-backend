# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0013_stripewebhooklog'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='popular',
            field=models.BooleanField(default=False),
        ),
    ]
