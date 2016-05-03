# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parentFolder', models.ForeignKey(to='reports.Folder', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('shortDescription', models.TextField(max_length=160)),
                ('longDescription', models.TextField()),
                ('timeStamp', models.DateTimeField(auto_now=True)),
                ('private', models.BooleanField(default=True)),
                ('keywords', models.TextField(default='', max_length=500)),
                ('collaborators', models.ManyToManyField(to=settings.AUTH_USER_MODEL, max_length=160)),
                ('files', models.ManyToManyField(blank=True, to='reports.File')),
                ('group', models.ForeignKey(to='auth.Group', related_name='group')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='reporter')),
            ],
        ),
        migrations.AddField(
            model_name='folder',
            name='reports',
            field=models.ManyToManyField(blank=True, to='reports.Report'),
        ),
    ]
