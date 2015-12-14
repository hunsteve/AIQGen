# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIQGen', '0003_problemintest_customscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='measuredheight',
            field=models.IntegerField(null=True),
        ),
    ]
