# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('test_intern', '0004_formforchosedepartment'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferedCourses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('AllCourses', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
    ]
