from django.shortcuts import render, redirect
from .forms import CustomUserForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest, HttpResponse
from typing import Dict, List

# Create your views here.


# creation d'un compte sur le site:
def registration(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form: CustomUserForm = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('main:home')
    else:
        form: CustomUserForm = CustomUserForm()
        ctx: Dict[str, CustomUserForm] = {'form':form}
        return render(request, 'my_auth/registration.html', ctx)
    

# moyen de logout du site:
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('main:home')

# Moyen de connexion :
def login_view(request: HttpRequest) ->HttpResponse:
    if request.method == 'POST':
        form: LoginForm = LoginForm(request.POST)
        if form.is_valid():
            your_username = form.cleaned_data['your_username']
            your_password = form.cleaned_data['your_password']
            user = authenticate(
                request,
                username = your_username,
                password = your_password
            )
            if user is not None:
                login(request,user)  
                return redirect('main:home')
            else:
                form.add_error(None, 'Invalids inputs !')       
    else: 
        form = LoginForm()

    ctx: Dict[str, LoginForm] = {'form':form}
    return render(request, 'my_auth/log_you.html', ctx)