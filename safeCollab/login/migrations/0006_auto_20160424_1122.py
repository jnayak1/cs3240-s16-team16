# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20160424_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(related_name='groups', to='auth.Group'),
        ),
    ]
