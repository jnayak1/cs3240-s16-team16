# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='keywords',
            field=models.TextField(default=datetime.datetime(2016, 5, 1, 21, 34, 21, 869942, tzinfo=utc), max_length=500),
            preserve_default=False,
        ),
    ]
