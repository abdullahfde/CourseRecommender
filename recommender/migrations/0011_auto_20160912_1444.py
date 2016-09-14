# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0010_auto_20160912_1314'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Curriculum',
            new_name='Curriculums',
        ),
        migrations.DeleteModel(
            name='CS',
        ),
        migrations.DeleteModel(
            name='EE',
        ),
        migrations.DeleteModel(
            name='IE',
        ),
    ]
