# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0018_profile_is_updated_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripe_subscription_id',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
