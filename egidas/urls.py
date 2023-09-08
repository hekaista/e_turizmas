from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search, name='search'),
    path('objektai/', views.PlaceListView.as_view(), name='place-list'),
    path('objektai/<int:pk>', views.PlaceDetailView.as_view(), name='place-detail')

]
