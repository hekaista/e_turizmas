from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profilis, OrderItem, TicketCopy
from datetime import datetime, timedelta


@receiver(post_save, sender=User)
def create_profile(sender,instance, created, **kwargs):
    if created:
        Profilis.objects.create(user=instance)


@receiver(post_save, sender=OrderItem)
def create_ticket_copies(sender, instance, created, **kwargs):
    if created:
        for _ in range(instance.quantity):
            TicketCopy.objects.create(
                ticket=instance.ticket,
                due_to=datetime.now() + timedelta(days=365)
            )
