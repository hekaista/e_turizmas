from django.shortcuts import render, get_object_or_404, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
#from .forms import BookReviewForm, UserUpdateForm, ProfilisUpdateForm, UserBookCreateForm


# from .models import
from .models import *

# Create your views here.

def index(request):
    num_places = Place.objects.all().count()
    num_reviews = Review.objects.all().count()
    num_orders = Order.objects.all().count()
    num_order_items = OrderItem.objects.all().count()
    num_tickets = Ticket.objects.all().count()

    context = {
        'num_places': num_places,
        'num_reviews': num_reviews,
        'num_orders': num_orders,
        'num_order_items': num_order_items,
        'num_tickets': num_tickets,
    }

    return render(request, 'index.html', context=context)


def search(request):
    query = request.GET.get('search_text')
    print(request.GET)
    search_results = Place.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query),
        Q(subcategories__icontains=query)
    )
    context = {
        'query': query,
        'search_results': search_results
    }
    return render(request, 'search.html', context=context)


class PlaceListView(generic.ListView):
    model = Place
    context_object_name = 'place_list'
    template_name = 'objektai.html'
    paginate_by = 8
