from django.shortcuts import render, redirect
from products.models import Product
from products.openfoodapi import OpenFoodAPI

from .forms import SearchBar

# Create your views here.

def search_products(request):
    print("Vue search_products")
    if request.method == "POST":
        form = SearchBar(request.POST or None)
        if form.is_valid():
            search_term = form.cleaned_data['content']
            print(search_term)

            return redirect('display_results', data=search_term)
    else:
        print("No term received")
        form = SearchBar()

    return render(request, 'products/index.html', locals())

def display_results(request, data):
    product = Product.objects.filter(name__contains=data)
    #if i find the asked product in base
    if product:
        #i first try to find 6 better products in base
        results = Product.objects.six_better_products(product[0])
        #if i find my products i return 'em to the template
        if results:
            return render(request, 'products/results.html', {
                'results':results,
            })
    # else i start a request on the web API
    else:
        pass
        # return redirect View api
        # product = OpenFoodAPI.return_six_healthy_prods(data)



#faire une deuxième vue dédiée à la recherche sur l'API