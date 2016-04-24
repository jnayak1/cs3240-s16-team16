# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0006_auto_20160424_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='collaborators',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, max_length=160),
        ),
    ]
