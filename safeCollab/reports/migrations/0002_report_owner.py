# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='owner',
            field=models.ForeignKey(related_name='reporter', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
