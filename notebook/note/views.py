from django.shortcuts import render
from .models import Inscription, Category

def index(request):
    return render(request, 'note/index.html')
