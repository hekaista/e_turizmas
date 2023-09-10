# Generated by Django 4.2.2 on 2023-09-09 07:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('egidas', '0014_remove_order_items_alter_orderitem_due_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='due_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 8, 10, 0, 40, 391326), null=True, verbose_name='Galojimas iki'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(blank=True, choices=[('Suaugusiam', 'Suaugusiems'), ('Vaikams', 'Vaikams'), ('Pens/Neįg', 'Neįgaliems ir pencininkams'), ('Bendrinis', 'Bendrinis'), ('Anykštėnams', 'Anykštėnams'), ('Stud/Moksl', 'Moksleiviams ir studentams')], default='Bendrinis', help_text='Bilieto tipas', max_length=50),
        ),
        migrations.CreateModel(
            name='Profilis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nuotrauka', models.ImageField(default='profile_pics/pfp.png', upload_to='profile_pics')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profilis',
                'verbose_name_plural': 'Profiliai',
            },
        ),
    ]
