# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIQGen', '0002_auto_20151206_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemintest',
            name='customscore',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
