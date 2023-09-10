from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('paieska/', views.search, name='search'),
    path('objektai/', views.PlaceListView.as_view(), name='place-list'),
    path('objektai/<int:pk>', views.PlaceDetailView.as_view(), name='place-detail'),
    path('profilis/', views.profile, name='profile'),
    path('registruotis/', views.register, name='register'),
    path('uzsakymai/<uuid:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('manouzsakymai/', views.UserOrderListView.as_view(), name='my-orders'),
    path('manouzsakymai/new', views.OrderByUserCreateView.as_view(), name='my-new-order'),
    path('manouzsakymai/<uuid:pk>/update', views.OrderByUserUpdateView.as_view(), name='my-order-update'),
    path('manouzsakymai/<uuid:pk>/delete', views.OrderByUserDeleteView.as_view(), name='my-order-delete'),
    path('prideti_pamegta/<int:place_id>/', views.add_favourite, name='add-favourite'),
    path('istrinti_pamegta/<int:place_id>/', views.remove_favourite, name='remove-favourite'),
    path('pamegti_objektai/', views.FavouriteListView.as_view(), name='favourites'),
]
