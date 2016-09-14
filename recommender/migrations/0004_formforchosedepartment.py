# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0003_curriculum'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormForChoseDepartment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('MyChoice', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
    ]
