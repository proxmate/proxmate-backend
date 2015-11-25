# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0010_paypalipnlog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='paypal_payment_id',
            new_name='paypal_payer_id',
        ),
    ]
