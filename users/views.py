from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .forms import RegisterForm, LoginForm
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def login_view(request):
    error = False

    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email=form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return render(request, 'products/index.html', locals())
            else:
                error = True

    form = LoginForm()
    return render(request, 'users/login.html', locals())


def register(request):

    form = RegisterForm(request.POST or None)
    error = False

    if form.is_valid():

        if form.cleaned_data['password'] == form.cleaned_data['password_check']:
            user = CustomUser.objects.create()
            user.first_name = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('/')
        else:
            error = True

    return render(request, 'users/register.html', locals())

def deconnect(request):
    logout(request)
    return redirect('/')


def profile(request, username):

    if request.user.is_authenticated and request.user.first_name == username:
        return render(request, 'users/profile.html', {'username': username})

    else:
        raise Http404


