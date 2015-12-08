# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cartitem_line_item_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='timestamps',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
    ]
