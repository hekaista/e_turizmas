from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail

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
        message = f'Jūsų užsakymas {instance.id} patvirtintas\n' \
                  f'Jūsų bilietai:\n'

        for ticket_copy in instance.ticket_copies.all():
            message += f"\nBilieto  ID: {ticket_copy.id}, " \
                       f"Pavadinimas: {ticket_copy.ticket.place}, {ticket_copy.ticket.service}, " \
                       f"Statusas: {ticket_copy.get_status_display()}, " \
                       f"Galioja iki: {ticket_copy.due_to}"

        send_mail(subject, message, 'info@epixel.lt', [instance.user.email])
