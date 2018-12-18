from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('register/',views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('logout/', views.deconnect, name='deconnect'),
    path('reset_password/', views.reset_password, name='reset_password'),
]