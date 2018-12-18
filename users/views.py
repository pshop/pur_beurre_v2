from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


from .forms import RegisterForm, LoginForm, PasswordResetForm, NewPasswordForm
from products.forms import SearchBar
from .models import CustomUser, ResetLink

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
            link = ResetLink(user=user)
            link.save()
            send_mail('nouveau mot de passe',
                      f"lien unique pour changer le mot de passe : <a href='http://127.0.0.1:8000/user/{link.link_id}'> LIEN <\\a>",
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

def type_new_password(request, link_id):
    form = SearchBar()
    new_password_form = NewPasswordForm(request.POST or None)
    password_dont_match = False
    password_updated = False

    link = get_object_or_404(ResetLink, link_id=link_id)
    user = CustomUser.objects.get(id=link.user_id)
    log.critical(f"UTILISATEUR: {user.first_name}")

    if new_password_form.is_valid():
        if new_password_form.cleaned_data['password'] == new_password_form.cleaned_data['password_check']:
            user.set_password(new_password_form.cleaned_data['password'])
            user.save()
            password_updated = True
            ResetLink.objects.filter(user_id=user.id).delete()
        else:
            password_dont_match = True



    return render(request, 'users/type_new_password.html',{
        'form': form,
        'new_password_form': new_password_form,
        'dont_match': password_dont_match,
        'password_updated': password_updated,
        'link_id': link_id,
    })
