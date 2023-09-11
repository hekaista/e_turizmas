from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q, Avg
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# from .forms import BookReviewForm, UserUpdateForm, ProfilisUpdateForm, UserBookCreateForm
from .models import Category, Subcategory, Place, Ticket, Order, OrderItem, PlaceReview, User, Favourite
from .forms import PlaceReviewForm, UserOrderCreateForm, UserUpdateForm, ProfilisUpdateForm, OrderItemFormSet


# Create your views here.

def index(request):
    num_places = Place.objects.all().count()
    num_reviews = PlaceReview.objects.all().count()
    num_orders = Order.objects.all().count()
    num_order_items = OrderItem.objects.all().count()
    num_tickets = Ticket.objects.all().count()

    username = request.user
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_places': num_places,
        'num_reviews': num_reviews,
        'num_orders': num_orders,
        'num_order_items': num_order_items,
        'num_tickets': num_tickets,
        'username': username,
        'num_visits': num_visits
    }
    if not request.user.is_authenticated:
        messages.info(request,
                      "Dar nesiregistravote? Užsiregistruokite ir gaukite prieigą prie bilietų pirkimo, "
                      "objektų įvertinimo ir atsiliepimų rašymo. Sukurkite savo mėgstamiausių sąrašą.")
    return render(request, 'index.html', context=context)


def search(request):
    query = request.GET.get('search_text')
    print(request.GET)
    search_results = Place.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(subcategories__name__icontains=query)
    ).distinct()
    context = {
        'query': query,
        'search_results': search_results
    }
    return render(request, 'search.html', context=context)


class PlaceListView(generic.ListView):
    model = Place
    template_name = 'place_list.html'
    context_object_name = 'place_list'
    paginate_by = 8

    def get_queryset(self):
        category_name = self.request.GET.get('category', None)
        subcategory_name = self.request.GET.get('subcategory', None)

        queryset = Place.objects.all()

        if category_name:
            queryset = queryset.filter(subcategories__category__name=category_name)

        if subcategory_name:
            queryset = queryset.filter(subcategories__name=subcategory_name)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        category_name = self.request.GET.get('category', None)
        subcategory_name = self.request.GET.get('subcategory', None)

        if subcategory_name:
            try:
                subcategory = Subcategory.objects.get(name=subcategory_name)
                category_name = subcategory.category.name
            except Subcategory.DoesNotExist:
                pass

        if category_name:
            subcategories = Subcategory.objects.filter(category__name=category_name)
            context['subcategories'] = subcategories

        return context


class PlaceDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Place
    context_object_name = 'place'
    template_name = 'place_detail.html'
    form_class = PlaceReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        average_rating = PlaceReview.objects.filter(place=self.object).aggregate(Avg('rating'))['rating__avg']
        if average_rating is None:
            average_rating = 'No ratings yet'
        context['average_rating'] = average_rating
        return context

    def get_success_url(self):
        return reverse('place-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.place = self.object
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'orders_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-date_created')


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'user_order_detail.html'

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    context_object_name = 'order_list'
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-purchase_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_list'] = context['page_obj']
        return context


class FavouriteListView(LoginRequiredMixin, generic.ListView):
    model = Favourite
    template_name = 'favourites.html'

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        # paimami duomenys iš formos
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Vartotojas Jau egzistuoja!")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Vartotojas su tokiu paštu {email} egzistuoja!")
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f"Vartotojas {username} sukurtas!")
                    return redirect('login')
    else:
        return render(request, "registration/registration.html")


@login_required
def profile(request):
    if request.method == "GET":
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)
    elif request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profilis atnaujintas")
            return redirect('profile')

    context_t = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context=context_t)


class OrderByUserCreateView(generic.CreateView):
    model = Order
    template_name = 'user_order_form.html'
    form_class = UserOrderCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST)
        else:
            context['formset'] = OrderItemFormSet()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        formset = self.get_context_data()['formset']

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('ticket') and form.cleaned_data.get('quantity'):
                    order_item = form.save(commit=False)
                    order_item.order = self.object
                    order_item.save()
        return redirect('/egidas/manouzsakymai')


class OrderByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                            generic.UpdateView):
    model = Order
    fields = ['status']
    success_url = '/egidas/manouzsakymai'
    template_name = 'user_order_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user


class OrderByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                            generic.DeleteView):
    model = Order
    template_name = 'user_order_delete.html'
    success_url = '/egidas/manouzsakymai'

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user


@login_required
def add_favourite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favourite.objects.get_or_create(user=request.user, place=place)
    return redirect('favourites')


@login_required
def remove_favourite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favourite.objects.filter(user=request.user, place=place).delete()
    return redirect('favourites')
