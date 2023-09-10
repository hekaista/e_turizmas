from django import forms
from .models import User, Profilis, PlaceReview, Order, Ticket, OrderItem
from django.forms import formset_factory


class PlaceReviewForm(forms.ModelForm):
    class Meta:
        model = PlaceReview
        fields = ('content', 'user')
        widgets = {
            'place': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Jūsų tekstas...'}),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']


class DateInput(forms.DateInput):
    input_type = 'date'


class UserOrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []



class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['ticket', 'quantity', ]


OrderItemFormSet = formset_factory(OrderItemForm, extra=1)
