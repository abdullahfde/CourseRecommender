# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0007_savingtrancript'),
    ]

    operations = [
        migrations.CreateModel(
            name='transcripts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('files', models.FileField(upload_to=b'transcripts')),
            ],
        ),
    ]
