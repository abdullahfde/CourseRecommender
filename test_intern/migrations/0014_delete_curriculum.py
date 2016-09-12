# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_intern', '0013_curriculum'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Curriculum',
        ),
    ]
