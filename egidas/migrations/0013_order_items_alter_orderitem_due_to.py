# Generated by Django 4.2.2 on 2023-09-07 15:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('egidas', '0012_remove_order_items_alter_orderitem_due_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='egidas.orderitem'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='due_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 6, 18, 54, 13, 424455), null=True, verbose_name='Galojimas iki'),
        ),
    ]