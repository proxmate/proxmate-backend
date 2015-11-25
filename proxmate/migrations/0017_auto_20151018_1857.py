# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxmate', '0016_message_time_shown'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentScript',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('match', models.CharField(default=b'', max_length=128, null=True, blank=True)),
                ('script', models.TextField(default=b'', null=True, blank=True)),
                ('package', models.ForeignKey(to='proxmate.Package')),
            ],
        ),
        migrations.RemoveField(
            model_name='contentscripts',
            name='country',
        ),
        migrations.DeleteModel(
            name='ContentScripts',
        ),
    ]
