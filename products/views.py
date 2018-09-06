from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchBar
from django.views.generic import TemplateView

# Create your views here.

def search_products(request):


    form = SearchBar(request.POST or None)

    if form.is_valid():
        search_term = form.cleaned_data['content']

        return HttpResponse(
            f"""
            <p>produit recherché : {search_term}<p>
            """
        )


