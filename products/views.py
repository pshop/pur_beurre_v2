from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SearchBar
import sys

# Create your views here.

def search_products(request):
    print("Vue search_products")
    if request.method == "POST":
        form = SearchBar(request.POST or None)
        if form.is_valid():
            search_term = form.cleaned_data['content']
            print(search_term)

            redirect('display_results', data=search_term)
    else:
        print("No term received")
        form = SearchBar()

    return render(request, 'products/index.html', locals())

def display_results(request, data):

    return HttpResponse(
        f"Vous cherchez {data}"
    )

