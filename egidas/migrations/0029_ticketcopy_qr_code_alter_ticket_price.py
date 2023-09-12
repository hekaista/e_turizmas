# Generated by Django 4.2.5 on 2023-09-12 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egidas', '0028_remove_ticketcopy_order_item_ticketcopy_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketcopy',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Kaina'),
        ),
    ]
