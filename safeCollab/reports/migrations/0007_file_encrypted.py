# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_auto_20160424_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='encrypted',
            field=models.BooleanField(default=True),
        ),
    ]
