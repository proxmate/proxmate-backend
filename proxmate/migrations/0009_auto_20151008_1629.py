# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0008_profile_subscription_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='paypal_payment_id',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='paypal_subscr_id',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='subscription_supplier',
            field=models.CharField(default=b'', max_length=128),
        ),
    ]
