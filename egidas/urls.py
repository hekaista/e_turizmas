from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('paieska/', views.search, name='search'),
    path('objektai/', views.PlaceListView.as_view(), name='place-list'),
    path('objektai/<int:pk>', views.PlaceDetailView.as_view(), name='place-detail'),
    path('profilis/', views.profile, name='profile'),
    path('registruotis/', views.register, name='register'),
    path('manouzsakymai/', views.UserOrderListView.as_view(), name='my-orders'),

]
