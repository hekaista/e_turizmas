from django.contrib import admin

# Register your models here.
from .models import Category, Subcategory, Place, Review, Favourite, Ticket, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category__name',)
    search_fields = ('name',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'get_subcategories', 'get_categories')

    def get_categories(self, obj):
        unique_categories = set(sub.category for sub in obj.subcategories.all())
        return ", ".join([str(cat) for cat in unique_categories])

    def get_subcategories(self, obj):
        return ", ".join([str(sub) for sub in obj.subcategories.all()])

    get_subcategories.short_description = 'Subcategorijos'
    get_categories.short_description = 'Kategorijos'

    list_editable = ('address',)
    list_filter = ('subcategories__category', 'subcategories')
    search_fields = ('title',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('place', 'price', 'service', 'type')
    list_filter = ('place', 'type')
    search_fields = ('place__title',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


# @admin.register(TicketCopy)
# class TicketCopyAdmin(admin.ModelAdmin):
#     list_display = ('id', 'ticket')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'purchase_date')
    list_filter = ('purchase_date',)
    search_fields = ('user__username', 'ticket__place__title')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'due_to', 'status')
    list_filter = ('status',)
    search_fields = ('id',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'rating')
    list_filter = ('place', 'rating')
    search_fields = ('user__username', 'place__title')


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'place')
    list_filter = ('user', 'place', 'place__subcategories__category', 'place__subcategories__name')
    search_fields = ('user__username', 'place__subcategories__name')
