# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0015_profile_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='time_shown',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
