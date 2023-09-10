# Generated by Django 4.2.2 on 2023-09-09 16:17

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('egidas', '0019_alter_orderitem_due_to_placereview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='placereview',
            options={'verbose_name': 'Atsiliepimas', 'verbose_name_plural': 'Atsiliepimai'},
        ),
        migrations.RemoveField(
            model_name='placereview',
            name='reviewer',
        ),
        migrations.AddField(
            model_name='placereview',
            name='rating',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Įvertinimas'),
        ),
        migrations.AddField(
            model_name='placereview',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Gautas', 'Gautas'), ('Ivykdytas', 'Ivykdytas'), ('Atšauktas', 'Atšauktas'), ('Laukiama apmokėjimo', 'Laukiama apmokėjimo')], default='Gautas', help_text='Užsakymo statusas', max_length=50),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='due_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 8, 19, 17, 0, 786971), null=True, verbose_name='Galojimas iki'),
        ),
        migrations.AlterField(
            model_name='placereview',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Atsiliepimas'),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
