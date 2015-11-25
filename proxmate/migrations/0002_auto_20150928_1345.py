# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='additional_countries',
            field=models.ManyToManyField(to='proxmate.Country'),
        ),
        migrations.AddField(
            model_name='package',
            name='allow_multiple_countries',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='country',
            field=models.ForeignKey(related_name='proxmate_package_related', to='proxmate.Country'),
        ),
    ]
