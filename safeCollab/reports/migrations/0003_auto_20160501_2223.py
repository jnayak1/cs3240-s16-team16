# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_report_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='keywords',
            field=models.TextField(default=b'', max_length=500),
        ),
    ]
