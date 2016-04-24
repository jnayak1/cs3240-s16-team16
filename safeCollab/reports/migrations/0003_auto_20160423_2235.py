# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('reports', '0002_report_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='collaborators',
        ),
        migrations.AddField(
            model_name='report',
            name='group',
            field=models.ForeignKey(to='auth.Group', default=''),
        ),
    ]
