# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0005_publickey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publickey',
            name='key',
            field=models.CharField(max_length=32),
        ),
    ]
