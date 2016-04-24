# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20160423_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='group',
            field=models.ForeignKey(to='auth.Group'),
        ),
    ]
