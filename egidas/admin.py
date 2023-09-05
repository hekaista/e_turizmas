from django.contrib import admin

# Register your models here.
from .models import Category, Subcategory, Place, Review, Favourite, Ticket, TicketOrder, TicketInstance


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'address']
    list_filter = ['subcategories']
    search_fields = ['title']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'place', 'rating']
    list_filter = ['place', 'rating']
    search_fields = ['user__username', 'place__title']


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'place']
    list_filter = ['user', 'place']
    search_fields = ['user__username', 'place__title']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['place', 'price', 'type']
    list_filter = ['place', 'type']
    search_fields = ['place__title']


@admin.register(TicketOrder)
class TicketOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket', 'quantity', 'purchase_date']
    list_filter = ['purchase_date']
    search_fields = ['user__username', 'ticket__place__title']


@admin.register(TicketInstance)
class TicketInstanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket_order', 'due_to', 'status']
    list_filter = ['status']
    search_fields = ['id', 'ticket_order__ticket__place__title']
