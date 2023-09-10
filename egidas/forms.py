from django import forms
from .models import User, Profilis, PlaceReview, Order


class PlaceReviewForm(forms.ModelForm):
    class Meta:
        model = PlaceReview
        fields = ('content', 'user')
        widgets = {
            'place': forms.HiddenInput(),
            'user': forms.HiddenInput()
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
        widgets = {
            'user': forms.HiddenInput(),
        }
