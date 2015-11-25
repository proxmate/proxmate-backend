# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0003_auto_20150930_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='additional_countries',
            field=models.ManyToManyField(to='proxmate.Country', blank=True),
        ),
    ]
