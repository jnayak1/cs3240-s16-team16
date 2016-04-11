# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('private_messages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversationlog',
            name='log',
        ),
        migrations.AddField(
            model_name='conversationlog',
            name='log',
            field=models.ManyToManyField(to='private_messages.Message'),
        ),
    ]
