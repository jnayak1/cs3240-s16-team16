# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
                ('title', models.CharField(max_length=50)),
                ('timeStamp', models.DateTimeField(auto_now=True)),
                ('content', models.BinaryField()),
                ('encrypted', models.BooleanField(default=True)),
                ('publisher', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parentFolder', models.ForeignKey(null=True, blank=True, to='reports.Folder')),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parentFolder', models.ForeignKey(blank=True, to='reports.Folder', null=True)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
                ('title', models.CharField(max_length=50)),
                ('shortDescription', models.TextField(max_length=160)),
                ('longDescription', models.TextField()),
                ('timeStamp', models.DateTimeField(auto_now=True)),
                ('private', models.BooleanField(default=True)),
<<<<<<< HEAD
                ('keywords', models.TextField(max_length=500, default='')),
                ('collaborators', models.ManyToManyField(max_length=160, to=settings.AUTH_USER_MODEL)),
                ('files', models.ManyToManyField(blank=True, to='reports.File')),
                ('group', models.ForeignKey(to='auth.Group', related_name='group')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='reporter')),
=======
                ('keywords', models.TextField(default=b'', max_length=500)),
                ('collaborators', models.ManyToManyField(to=settings.AUTH_USER_MODEL, max_length=160)),
                ('files', models.ManyToManyField(to='reports.File', blank=True)),
                ('group', models.ForeignKey(related_name='group', to='auth.Group')),
                ('owner', models.ForeignKey(related_name='reporter', to=settings.AUTH_USER_MODEL)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
            ],
        ),
        migrations.AddField(
            model_name='folder',
            name='reports',
            field=models.ManyToManyField(to='reports.Report', blank=True),
        ),
    ]
