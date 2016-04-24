# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20160423_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='group',
            field=models.ForeignKey(default='placeholder', to='auth.Group'),
        ),
    ]
