# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('login', '0003_report_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(to='auth.Group'),
        ),
    ]
