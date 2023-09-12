# Generated by Django 4.2.5 on 2023-09-11 16:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('egidas', '0023_alter_orderitem_options_remove_order_items_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='ticket_copy',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('G', 'Galiojantis'), ('P', 'Panaudotas'), ('N', 'Nebegalioja'), ('A', 'Atšauktas')], default='G', max_length=1),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='TicketCopy',
        ),
    ]
