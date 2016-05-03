# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversationLog',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
                ('content', models.BinaryField()),
                ('encrypted', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='conversationlog',
            name='log',
            field=models.ManyToManyField(to='private_messages.Message'),
        ),
        migrations.AddField(
            model_name='conversationlog',
            name='participants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conversationlog',
            name='readBy',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='readBy'),
        ),
    ]
