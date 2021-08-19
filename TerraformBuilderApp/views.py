from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CreateUserForm, LoginForm


def home(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'TerraformBuilderApp/dashboard.html', context)
    else:
        return redirect('login')


def log_in(request):
    if not request.user.is_authenticated:
        form = LoginForm()
        context = {'form': form}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Username or password is incorrect !")
                return render(request, 'TerraformBuilderApp/login.html', context)
        else:
            return render(request, 'TerraformBuilderApp/login.html', context)
    else:
        return redirect('/')


def log_out(request):
    logout(request)
    return redirect('login')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'TerraformBuilderApp/register.html', context)
