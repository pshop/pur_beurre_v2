from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.contrib import messages

import openfoodfacts
import logging
import unidecode
from pprint import pformat

from .forms import SearchBar
from .models import Product
from .openfoodapi import OpenFoodAPI


log = logging.getLogger(__name__)


def search_products(request):

    if request.method == "POST":
        form = SearchBar(request.POST or None)
        if form.is_valid():
            search_term = form.cleaned_data['content']
            # I have issues with accenduated characters
            search_term = unidecode.unidecode(search_term)
            return redirect('display_results', data=search_term)
    else:
        form = SearchBar()

    return render(request, 'products/index.html', {
        'form': form,
    })


def display_results(request, data):
    product = Product.objects.filter(name__contains=data)
    log.critical(f"product = {product}")
    form = SearchBar()
    open_food = OpenFoodAPI()
    results = []
    # if i find the asked product in base
    if product:
        # i first try to find 6 better products in base
        results = Product.objects.six_better_products(product[0])
        # if i find my products i return 'em to the template
    if not results:
        # else i start a request on the web API
        results = open_food.return_six_healthy_prods(data)

    searched_prod = open_food.search_product(data)

    if searched_prod:
        return render(request, 'products/results.html', {
            'results': results,
            'form': form,
            'searched_prod': searched_prod,
            'error': False
        })
    else:
        messages.error(request, f"Aucun résultat trouvé pour {data}")
        return redirect('search')



def product_info(request, product_id):
    form = SearchBar()
    open_food = OpenFoodAPI()
    error = False

    try:
        product = Product.objects.get(id=product_id)
        product = model_to_dict(product)
    except:
        try:
            product = openfoodfacts.products.get_product(product_id)
            product = open_food.clean_prod_info(product['product'])
        except:
            error = True

    if product['nutriscore'] is not 'e':
        nutriscore_img = f"nutriscore-{product['nutriscore']}.svg"
    else:
        nutriscore_img = None

    return render(request,
                  'products/product.html',
                  {
                      'form': form,
                      'prod': product,
                      'nutriscore_img': nutriscore_img,
                      'error': error,
                  })

def save_product(request, product_id):

    open_food = OpenFoodAPI()

    product = openfoodfacts.products.get_product(product_id)
    product = open_food.clean_prod_info(product['product'])

    product, created = Product.objects.get_or_create(
        id=int(product_id),
        nutriscore=product['nutriscore'],
        name=product['name'],
        summation=product['summation'],
        picture=product['picture'],
        nutrition=product['nutrition'],
    )

    product.user.add(request.user)
    product.save()

    messages.success(request, "le produit à bien été sauvegardé")
    return redirect(product_info, product_id)

def display_favorites(request, user_name):
    form = SearchBar()
    products = Product.objects.filter(user__first_name=user_name)
    return render(request,
                  'products/favorites.html',
                  {
                      'results': products,
                      'form': form,
                  })



