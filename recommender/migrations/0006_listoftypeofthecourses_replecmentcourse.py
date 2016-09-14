# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0005_offeredcourses'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListOfTypeOfTheCourses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ListOfTypeOfTheCourses', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='ReplecmentCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ReplecmentCourse', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
    ]
