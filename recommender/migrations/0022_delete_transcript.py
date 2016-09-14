# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0021_delete_mgt'),
    ]

    operations = [
        migrations.DeleteModel(
            name='transcript',
        ),
    ]
