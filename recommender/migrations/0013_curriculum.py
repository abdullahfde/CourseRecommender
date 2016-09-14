# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0012_delete_curriculums'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Curriculums', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
    ]
