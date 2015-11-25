# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0011_auto_20151008_1705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='email',
            new_name='payer_email',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='theplan',
            new_name='subscription_id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='charge_id',
            new_name='transaction_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='currency',
            field=models.CharField(max_length=3, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='subscription_plan',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
