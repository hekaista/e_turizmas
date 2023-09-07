from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from tinymce.models import HTMLField
import uuid
from datetime import datetime, date, timedelta

class Category(models.Model):
    name = models.CharField('Kategorija', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategorija'
        verbose_name_plural = 'Kategorijos'


class Subcategory(models.Model):
    name = models.CharField('Subkategorija', max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Subkategorija'
        verbose_name_plural = 'Subkategorijos'


# Place Model
class Place(models.Model):
    title = models.CharField('Pavadinimas', max_length=200)
    address = models.CharField("Adresas", max_length=200, null=True, blank=True)
    latitude = models.FloatField("Platuma", null=True, blank=True)
    longitude = models.FloatField("Ilguma", null=True, blank=True)
    description = HTMLField("Apie")
    working_hours = models.CharField('Darbo valandos', max_length=255, null=True, blank=True)
    tel = models.CharField('Telefono numeris', max_length=20)
    website = models.URLField('Svetainė', max_length=200, null=True, blank=True)
    subcategories = models.ManyToManyField(Subcategory, related_name='places', help_text='Priskirkite subkategorijas')
    cover = models.ImageField("Nuotrauka", upload_to="covers", null=True)

    # favourited_by = models.ManyToManyField(User, related_name='favourite_places')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Objektas'
        verbose_name_plural = 'Objektai'


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    place = models.ForeignKey(Place, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField('Atsiliepimas', null=True, blank=True)
    rating = models.IntegerField('Įvertinimas', validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user.username}  atsiliepimas apie {self.place.title}"

    class Meta:
        verbose_name = 'Atsiliepimas'
        verbose_name_plural = 'Atsiliepimai'


class Favourite(models.Model):
    user = models.ForeignKey(User, related_name='favourites', on_delete=models.CASCADE)
    place = models.ForeignKey(Place, related_name='favourites', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'place')  # Kad vartotojas negalėtų dubliuoti objektų savo mėgstamų saraše
        verbose_name = 'Pamėgtas'
        verbose_name_plural = 'Pamėgti'

    def __str__(self):
        return f"{self.place.title}"


class Ticket(models.Model):
    place = models.ForeignKey(Place, related_name='tickets', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    service = models.CharField('Paslaugos pavadinimas', max_length=255, null=True, blank=True)
    TYPE = (
        ('Suaugusiam', 'Suaugusiems'),
        ('Vaikams', 'Vaikams'),
        ('Pens/Neįg', 'Neįgaliems ir pencininkams'),
        ('Bendrinis', 'Bendrinis'),
        ('Anykštėnui', 'Anykštėnams'),
        ('Stud/Moksl', 'Moksleiviams ir studentams')
    )

    type = models.CharField(
        max_length=50,
        choices=TYPE,
        blank=True,
        default='Bendrinis',
        help_text='Bilieto tipas'
    )

    def __str__(self):
        return f"Bilietas {self.type} į {self.place.title}, {self.price}"

    class Meta:
        verbose_name = 'Bilietas'
        verbose_name_plural = 'Bilietai'


class TicketOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='ticket_purchases', on_delete=models.CASCADE)
    #ticket = models.ForeignKey(Ticket, related_name='purchases', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField('Pirkimo data', auto_now_add=True)
    total = models.IntegerField('Suma viso:', null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.user}"

    class Meta:
        ordering = ['purchase_date']
        verbose_name = 'Bilieto užsalymas'
        verbose_name_plural = 'Bilietų užsakymai'


class TicketInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(TicketOrder, related_name='ticket_Instances', on_delete=models.CASCADE,null=True, blank=True)
    ticket = models.ForeignKey(Ticket, related_name='ticket_Instances', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('Kiekis', null=True, blank=True)
    due_to = models.DateTimeField('Galojimas iki', default=datetime.now() + timedelta(days=365), null=True, blank=True)

    STATUS = [
        ('G', 'Galiojantis'),
        ('P', 'Panaudotas'),
        ('N', 'Nebegalioja'),
        ('A', 'Atšauktas'),
    ]

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default='G',
    )

    @property
    def is_overdue(self):
        if self.due_to and date.today() > self.due_to:
            return True
        else:
            return False

    @property
    def eilutes_total(self):
        return self.quantity * self.ticket.price

    class Meta:

        ordering = ['due_to']
        verbose_name = 'Bilieto egzempliorius'
        verbose_name_plural = 'Bilietų egzemplioriai'

    def __str__(self):
        return f"Ūnikalus bilietas {self.id} į {self.ticket.place}, {self.ticket.service}"
