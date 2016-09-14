# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0017_curriculum'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReplecmentCourse',
        ),
    ]
