from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def login_view(request):
    error = False

    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username=form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                error = True
    else:
        form = LoginForm()

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

def deconnect(request):
    logout(request)
    return redirect('/')


def profile(request):
    pass