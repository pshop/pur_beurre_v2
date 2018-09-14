from django.urls import path
from django.contrib.auth import views as auth_views
from products import views

urlpatterns = [
    path('', views.search_products, name='search'),
    path('result/<data>', views.display_results, name='display_results' ),
    #path('result/', views.display_results, name='display_results' ),
]