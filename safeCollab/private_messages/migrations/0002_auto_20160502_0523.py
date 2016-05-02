# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('private_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationlog',
            name='readBy',
            field=models.ManyToManyField(related_name='readBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='encrypted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.BinaryField(),
        ),
    ]
