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
            name='ActivateUser',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
                ('username', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=128, unique=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='DeactivateUser',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
                ('username', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DeleteUser',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
                ('username', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Groupings',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
                ('title', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('views', models.IntegerField(default=0)),
                ('category', models.ForeignKey(to='login.Category')),
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
                ('description', models.CharField(max_length=128)),
                ('detailed_description', models.CharField(max_length=255)),
                ('public', models.BooleanField(default=0)),
                ('tags', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SiteManager',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
                ('name', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('user_type', models.CharField(max_length=16)),
                ('public_key', models.CharField(max_length=271)),
                ('groups', models.ManyToManyField(to='auth.Group', related_name='groups')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user')),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('user_type', models.CharField(max_length=16)),
                ('public_key', models.CharField(max_length=271)),
                ('groups', models.ManyToManyField(related_name='groups', to='auth.Group')),
                ('user', models.OneToOneField(related_name='user', to=settings.AUTH_USER_MODEL)),
>>>>>>> ee051a211cd124b1183d45a3943a0891c7733a3a
            ],
        ),
    ]
