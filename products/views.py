from django.shortcuts import render, redirect
from products.models import Product
from products.openfoodapi import OpenFoodAPI
import openfoodfacts
import sys

from .forms import SearchBar

# Create your views here.


def search_products(request):
    if request.method == "POST":
        form = SearchBar(request.POST or None)
        if form.is_valid():
            search_term = form.cleaned_data['content']
            print(search_term)

            return redirect('display_results', data=search_term)
    else:
        form = SearchBar()

    return render(request, 'products/index.html', {
        'form': form,
    })


def display_results(request, data):
    product = Product.objects.filter(name__contains=data)
    form = SearchBar()
    open_food = OpenFoodAPI()
    # if i find the asked product in base
    if product:
        # i first try to find 6 better products in base
        results = Product.objects.six_better_products(product[0])

        # if i find my products i return 'em to the template
    else:
        # else i start a request on the web API
        results = open_food.return_six_healthy_prods(data)

    searched_prod = open_food.search_product(data)
    return render(request, 'products/results.html', {
        'results': results,
        'form': form,
        'searched_prod': searched_prod,
    })


def product_info(request, product_id):
    form = SearchBar()
    open_food = OpenFoodAPI()
    error = False

    prod = Product.objects.get(id=product_id)

    if not prod:
        try:
            prod = openfoodfacts.products.get_product(product_id)
            prod = open_food.clean_prod_info(prod)
        except:
            error = True

    return render(request,
                  'products/product.html',
                  {
                      'form': form,
                      'prod': prod,
                  })
