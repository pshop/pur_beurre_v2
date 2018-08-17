from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from core_app.models import CustomUser
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
            else:
                error = True
    else:
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


def profile(request):
    pass