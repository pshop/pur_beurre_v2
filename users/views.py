from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail


from .forms import RegisterForm, LoginForm, PasswordResetForm
from products.forms import SearchBar
from .models import CustomUser

import logging

log = logging.getLogger(__name__)


# Create your views here.


def login_view(request):
    form = SearchBar()

    error = False

    if request.method == "POST":
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user and user.first_name:
                login(request, user)
                form = SearchBar()
                return render(request, 'products/index.html', locals())
            else:
                error = True

    login_form = LoginForm()
    return render(request, 'users/login.html', {
        'login_form': login_form,
        'error': error,
        'form': form,
    })


def register(request):
    form = SearchBar()
    register_form = RegisterForm(request.POST or None)
    error = False

    if register_form.is_valid():

        if register_form.cleaned_data['password'] == register_form.cleaned_data['password_check']:
            user = CustomUser.objects.create()
            user.first_name = register_form.cleaned_data['username']
            user.set_password(register_form.cleaned_data['password'])
            user.email = register_form.cleaned_data['email']
            user.save()
            user = authenticate(username=register_form.cleaned_data['email'], password=register_form.cleaned_data['password'])
            login(request, user)
            return redirect('/')
        else:
            error = True

    return render(request, 'users/register.html', locals())


def deconnect(request):
    logout(request)
    return redirect('/')


def profile(request, username='superuser'):
    form = SearchBar()
    if request.user.is_authenticated and request.user.first_name == username:
        return render(request, 'users/profile.html', {
            'username': username,
            'form': form})

    else:
        raise Http404

def reset_password(request):
    form = SearchBar()
    password_reset_form = PasswordResetForm(request.POST or None)
    form_validated = False

    if password_reset_form.is_valid():
        try:
            user = CustomUser.objects.get(email=password_reset_form.cleaned_data['email'])
            log.critical(f"utilisateur trouvé {user}")
            send_mail('nouveau mot de passe',
                      'lien unique pour changer le mot de passe',
                      'from@exempale.com',
                      [user.email],
                      fail_silently=False,
            )
            form_validated = True
        except ObjectDoesNotExist:
            form_validated = True



    return render(request, 'users/password_reset_form.html', {
        'form': form,
        'password_reset_form': password_reset_form,
        'form_validated': form_validated,
    })


