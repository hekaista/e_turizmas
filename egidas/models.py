from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from tinymce.models import HTMLField
import uuid
from PIL import Image
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
    cover = models.ImageField("Nuotrauka", upload_to="covers", null=True, blank=True)

    # favourited_by = models.ManyToManyField(User, related_name='favourite_places')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Objektas'
        verbose_name_plural = 'Objektai'


class PlaceReview(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="placereview_set", blank=True)
    content = models.TextField('Atsiliepimas', null=True, blank=True)
    rating = models.IntegerField('Įvertinimas', null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.content}'

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
        ('Anykštėnams', 'Anykštėnams'),
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


# class TicketCopy(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_date = models.DateTimeField('Pirkimo data', auto_now_add=True)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)

    # items = models.ForeignKey("OrderItem", related_name='orders', on_delete=models.CASCADE, null=True, blank=True)
    # total = models.IntegerField('Suma viso:', null=True, blank=True)
    ORDER_STATUS = (
        ('Gautas', 'Gautas'),
        ('Ivykdytas', 'Ivykdytas'),
        ('Atšauktas', 'Atšauktas'),
        ('Laukiama apmokėjimo', 'Laukiama apmokėjimo')
    )
    status = models.CharField(
        max_length=50,
        choices=ORDER_STATUS,
        blank=True,
        default='Gautas',
        help_text='Užsakymo statusas'
    )

    def get_total_sum(self):
        total = 0
        for item in self.order_items.all():
            total += item.get_total_price()
        return total

    def __str__(self):
        return f"{self.id} {self.user}"

    class Meta:
        ordering = ['purchase_date']
        verbose_name = 'Užsalymas'
        verbose_name_plural = 'užsakymai'


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='Order_items', on_delete=models.CASCADE, null=True, blank=True)
    ticket = models.ForeignKey(Ticket, related_name='Order_items', on_delete=models.CASCADE, null=True,
                               blank=True)
    quantity = models.PositiveIntegerField("Kiekis", default=1)
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
    def get_total_price(self):
        return self.quantity * self.ticket.price if self.ticket and self.ticket.price else 0

    class Meta:

        ordering = ['due_to']
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'

    def __str__(self):
        return f"Ūnikalus bilietas {self.id} į {self.ticket.place}, {self.ticket.service}"


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    nuotrauka = models.ImageField(default='profile_pics/pfp.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} profilis"

    class Meta:
        verbose_name = 'Profilis'
        verbose_name_plural = 'Profiliai'

    # User nuotraukos pridėjimas ir dydžio keitimas, naujojam PIL biblioteka
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if (img.height > 300) or (img.width > 300):
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)
