# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0003_auto_20160409_2343'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UploadFile',
        ),
    ]
