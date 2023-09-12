from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Profilis, OrderItem, TicketCopy, Order
from datetime import datetime, timedelta


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profilis.objects.create(user=instance)


@receiver(post_save, sender=OrderItem)
def create_ticket_copies(sender, instance, created, **kwargs):
    if created and instance.order:
        for _ in range(instance.quantity):
            TicketCopy.objects.create(
                ticket=instance.ticket,
                due_to=datetime.now() + timedelta(days=365),
                order=instance.order
            )

@receiver(post_save, sender=Order)
def send_confirmation_email(sender, instance, **kwargs):
    if instance.status == 'Ivykdytas':
        subject = f'Jūsų užsakymas patvirtintas'
        html_content = render_to_string(
            'order_confirmation.html',
            {
                'order_id': instance.id,
                'ticket_copies': instance.ticket_copies.all()
            }
        )
        email = EmailMessage(
            subject,
            html_content,
            'info@epixel.lt',
            [instance.user.email]
        )
        email.content_subtype = 'html'
        email.send()
