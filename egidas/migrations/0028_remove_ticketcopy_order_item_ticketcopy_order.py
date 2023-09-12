# Generated by Django 4.2.5 on 2023-09-12 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('egidas', '0027_alter_ticketcopy_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketcopy',
            name='order_item',
        ),
        migrations.AddField(
            model_name='ticketcopy',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_copies', to='egidas.order'),
        ),
    ]
