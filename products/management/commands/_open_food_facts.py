import json
from sys import stdout
import openfoodfacts

class OpenFoodFacts():

    def add_nutella_categories(self):

        search_result = openfoodfacts.products.advanced_search({
            "search_terms":'nutella',
            "page_size": "1",
        })

        cat_list = []

        for cat in search_result['products'][0]['categories_tags']:
            cat_list.append(cat.split(':')[-1])

        return cat_list