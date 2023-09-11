from django.contrib import admin

# Register your models here.
from .models import Category, Subcategory, Place, PlaceReview, \
    Favourite, Ticket, Order, OrderItem, Profilis, TicketCopy


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category__name',)
    search_fields = ('name',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'get_subcategories', 'get_categories')
    list_editable = ('address',)
    list_filter = ('subcategories__category', 'subcategories')
    search_fields = ('title',)

    def get_categories(self, obj):
        unique_categories = set(sub.category for sub in obj.subcategories.all())
        return ", ".join([str(cat) for cat in unique_categories])

    def get_subcategories(self, obj):
        return ", ".join([str(sub) for sub in obj.subcategories.all()])

    get_subcategories.short_description = 'Subcategorijos'
    get_categories.short_description = 'Kategorijos'

class TicketCopyInline(admin.TabularInline):
    model = TicketCopy
    extra = 1
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('place', 'price', 'service', 'type')
    list_filter = ('place', 'type')
    search_fields = ('place__title',)
    inlines = [TicketCopyInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(TicketCopy)
class TicketCopyAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_place_title', 'due_to', 'status',)
    list_filter = ('status', 'due_to')

    def get_place_title(self, obj):
        return obj.ticket.place.title

    get_place_title.admin_order_field = 'ticket__place__title'
    get_place_title.short_description = 'Place Title'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'purchase_date', 'status')
    list_filter = ('purchase_date', 'status')
    list_editable = ('status',)
    search_fields = ('user__username',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('get_place_title', 'get_service', 'quantity')
    list_filter = ('ticket__place',)
    search_fields = ('order__id',)

    def get_place_title(self, obj):
        return obj.ticket.place.title

    get_place_title.admin_order_field = 'ticket__place__title'
    get_place_title.short_description = 'Place Title'

    def get_service(self, obj):
        return obj.ticket.service

    get_service.admin_order_field = 'ticket__service'
    get_service.short_description = 'Service'


@admin.register(PlaceReview)
class PlaceReviewAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'user', 'place', 'rating')
    list_filter = ('place', 'rating', 'date_created')
    search_fields = ('user__username', 'place__title')


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'place')
    list_filter = ('user', 'place', 'place__subcategories__category', 'place__subcategories__name')
    search_fields = ('user__username', 'place__subcategories__name')


admin.site.register(Profilis)
