# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentScripts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=128, null=True, blank=True)),
                ('port', models.CharField(max_length=128, null=True, blank=True)),
                ('user', models.CharField(max_length=256, null=True, blank=True)),
                ('password', models.CharField(max_length=256, null=True, blank=True)),
                ('ip', models.CharField(max_length=256, null=True, blank=True)),
                ('require_key', models.BooleanField(default=True)),
                ('is_private', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('version', models.CharField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, null=True, blank=True)),
                ('flag', models.ImageField(help_text=b'Please upload an image (.jpg, .png, .gif).', upload_to=b'flags')),
                ('short_hand', models.CharField(max_length=2, null=True, blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('title', models.CharField(default=b'Message Title', max_length=256)),
                ('content', models.TextField(default=b'Message Content', blank=True)),
                ('has_url', models.BooleanField(default=False)),
                ('is_sticky', models.BooleanField(default=False)),
                ('is_persistent', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('url', models.CharField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=128, null=True, blank=True)),
                ('name', models.CharField(default=b'', max_length=128, blank=True)),
                ('page_url', models.CharField(max_length=128, null=True, blank=True)),
                ('big_icon', models.ImageField(help_text=b'Please upload an image (.jpg, .png, .gif).', upload_to=b'big_icons')),
                ('small_icon', models.ImageField(help_text=b'Please upload an image (.jpg, .png, .gif).', upload_to=b'small_icons')),
                ('created_at', models.DateTimeField(null=True)),
                ('description', models.TextField(null=True)),
                ('require_key', models.BooleanField(default=True)),
                ('is_private', models.BooleanField(default=True)),
                ('country', models.ForeignKey(to='proxmate.Country')),
            ],
        ),
        migrations.CreateModel(
            name='PackageHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(default=b'', max_length=120)),
                ('package', models.ForeignKey(to='proxmate.Package')),
            ],
        ),
        migrations.CreateModel(
            name='PackageRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('route', models.CharField(default=b'', max_length=120)),
                ('type', models.CharField(default=b'host', help_text=b'The default currency for this advertiser', max_length=25, choices=[(b'startsWith', b'startsWith'), (b'host', b'host'), (b'contains', b'contains')])),
                ('package', models.ForeignKey(to='proxmate.Package')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charge_id', models.CharField(max_length=128, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.CharField(max_length=256, null=True, blank=True)),
                ('theplan', models.CharField(max_length=64, null=True, blank=True)),
                ('amount', models.CharField(max_length=16, null=True, blank=True)),
                ('description', models.CharField(max_length=256, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stripe_customer_id', models.TextField(null=True, blank=True)),
                ('activation_code', models.CharField(max_length=256, null=True, blank=True)),
                ('plan_expiration_date', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User status information',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=128, null=True, blank=True)),
                ('port', models.CharField(max_length=128, null=True, blank=True)),
                ('user', models.CharField(max_length=256, null=True, blank=True)),
                ('password', models.CharField(max_length=256, null=True, blank=True)),
                ('ip', models.CharField(max_length=256, null=True, blank=True)),
                ('require_key', models.BooleanField(default=True)),
                ('is_private', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('version', models.CharField(max_length=256, null=True, blank=True)),
                ('country', models.ForeignKey(to='proxmate.Country')),
            ],
        ),
        migrations.AddField(
            model_name='contentscripts',
            name='country',
            field=models.ForeignKey(to='proxmate.Country'),
        ),
    ]
