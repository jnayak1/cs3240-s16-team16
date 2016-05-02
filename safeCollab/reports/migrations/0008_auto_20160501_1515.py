# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_file_encrypted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='content',
            field=models.BinaryField(),
        ),
    ]
