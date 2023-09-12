from django import forms
from .models import User, Profilis, PlaceReview, Order, Ticket, OrderItem
from django.forms import formset_factory


class PlaceReviewForm(forms.ModelForm):
    class Meta:
        model = PlaceReview
        fields = ('content', 'rating', 'user',)
        widgets = {
            'place': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Jūsų tekstas...'}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'})
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
        fields = ['ticket', 'quantity']

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['ticket'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control quantity-input'})


OrderItemFormSet = formset_factory(OrderItemForm, extra=3)
