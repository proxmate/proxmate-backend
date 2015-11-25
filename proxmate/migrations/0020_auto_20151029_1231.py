# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0019_profile_stripe_subscription_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.CharField(default=b'', max_length=64, null=True, blank=True)),
                ('avg_first_response', models.IntegerField(default=0, null=True, blank=True)),
                ('avg_resolution', models.IntegerField(default=0, null=True, blank=True)),
                ('avg_replies', models.IntegerField(default=0, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='package',
            name='return_type',
            field=models.CharField(default=b'PROXY', max_length=128, blank=True),
        ),
    ]
