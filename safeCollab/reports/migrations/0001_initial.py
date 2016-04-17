# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=50)),
                ('timeStamp', models.DateTimeField(auto_now=True)),
                ('content', models.FileField(upload_to='files')),
                ('publisher', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HomeFolder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=50)),
                ('shortDescription', models.TextField(max_length=160)),
                ('longDescription', models.TextField()),
                ('timeStamp', models.DateTimeField(auto_now=True)),
                ('private', models.BooleanField(default=True)),
                ('collaborators', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('files', models.ManyToManyField(blank=True, to='reports.File')),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('homefolder_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, primary_key=True, to='reports.HomeFolder')),
            ],
            bases=('reports.homefolder',),
        ),
        migrations.AddField(
            model_name='report',
            name='parentFolder',
            field=models.ForeignKey(to='reports.HomeFolder'),
        ),
        migrations.AddField(
            model_name='homefolder',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='homefolder',
            name='reports',
            field=models.ManyToManyField(blank=True, to='reports.Report'),
        ),
        migrations.AddField(
            model_name='homefolder',
            name='subFolders',
            field=models.ManyToManyField(blank=True, to='reports.Folder'),
        ),
        migrations.AddField(
            model_name='folder',
            name='parentFolder',
            field=models.ForeignKey(to='reports.HomeFolder', related_name='hi'),
        ),
    ]
