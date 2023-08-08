from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# Create your views here.
def home(request):
    return render(request, 'map/home.html')