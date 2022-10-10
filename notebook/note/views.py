from django.shortcuts import render, redirect
from .models import Inscription, Category
from django.contrib.auth.forms import User
from django.contrib import messages

def index(request):
    return render(request, 'note/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('note:register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('note:register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, 'Registracija sėkminga')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('note:register')

    return render(request, 'note/register.html')