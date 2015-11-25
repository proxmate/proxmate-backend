# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0020_auto_20151029_1231'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reports',
        ),
    ]
