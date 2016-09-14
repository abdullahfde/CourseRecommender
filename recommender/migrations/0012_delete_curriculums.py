# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0011_auto_20160912_1444'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Curriculums',
        ),
    ]
