from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def login(request):
    return render(request, 'users/login.html', locals())

def register(request):

    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = User.objects.create()
        user.username = form.cleaned_data['username']
        user.set_password(form.cleaned_data['password'])
        user.email = form.cleaned_data['email']
        user.save()

        return redirect('/')

    else:
        return render(request, 'users/register.html', locals())


def profile(request):
    pass