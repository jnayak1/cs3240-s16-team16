# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_report_collaborators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='group',
            field=models.ForeignKey(related_name='group', to='auth.Group', null=True),
        ),
    ]
