# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIQGen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemInTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customspacing', models.FloatField()),
                ('problem', models.ForeignKey(to='AIQGen.Problem')),
            ],
        ),
        migrations.RemoveField(
            model_name='test',
            name='problems',
        ),
        migrations.AddField(
            model_name='problemintest',
            name='test',
            field=models.ForeignKey(to='AIQGen.Test'),
        ),
    ]
