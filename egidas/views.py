from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.views import generic
# from .models import
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    return render(request, 'index.html')
