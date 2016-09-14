# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0008_transcripts'),
    ]

    operations = [
        migrations.CreateModel(
            name='transcript',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Saving', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
        migrations.DeleteModel(
            name='transcripts',
        ),
    ]
