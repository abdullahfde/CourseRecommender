# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0020_delete_listoftypeofthecourses'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MGT',
        ),
    ]