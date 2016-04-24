# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20160423_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='group',
            field=models.ForeignKey(to='auth.Group', related_name='group'),
        ),
    ]
