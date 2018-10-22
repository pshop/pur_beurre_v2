# -*- coding: utf-8 -*

import requests
import re
import sys
from termcolor import colored
import logging
import pprint

from products.models import Product, Category, Specificity

log = logging.getLogger(__name__)

def test_image_url(url):
    """
    Test if an url is written the right way
    if it returns a http 200 response
    If the pointed file is a valid image format
    :param url:
    Entrer a string(url)
    :return:
    True if url is valid
    """
    regex = r"(^http|https)(://)(.*)(\.)(jpg|jpeg|png)"

    if re.match(regex, url) is not None:
        r = requests.get(url)
        if r.status_code == 200:
            return True
    else:
        return False




class OpenFoodFacts():

    def get_nutella_categories(self):

        result = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params={
            "search_terms": 'nutella',
            "page_size": "1",
            "json": "1",
        }).json()

        cat_list = []
        for cat in result['products'][0]['categories_hierarchy']:
            cat_name = cat.split(':')[-1]
            cat_list.append(cat_name.replace('-', ' '))

        return cat_list

    def get_products_by_category(self, category):

        search_result = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params={
            "search_terms":"",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "sort_by": "unique_scans",
            "page_size": "1000",
            "json": "1",
        }).json()

        # counter for 10 products of each grades category :
        a_b_grade = 0
        c_e_garde = 0

        #tuple of needed keys
        keys = ('id',
                'nutrition_grades',
                'product_name',
                'generic_name',
                'image_front_url',
                'image_nutrition_url',
                'url',
                'categories_hierarchy',
                )
        counter = 1
        sys.stdout.write(f" !!! {len(search_result['products'])} résultats obtenus pour {category}\n")

        for product in search_result['products']:

            sys.stdout.write(colored(f"produit numero {counter}\n", 'blue'))
            counter += 1

            # if i got enough products i break the for loop
            if a_b_grade > 10 and c_e_garde > 10:
                sys.stdout.write(colored(f"nous avons assez de produits\n\n", 'red'))
                break

            # i check if the product has all the needed keys
            if all(key in product for key in keys):

                sys.stdout.write(colored(f"Le produit {product['product_name']} id: {product['id']} contient les clés necessaires\n", 'green'))

                sys.stdout.write("CAT COUNTER:\n")
                sys.stdout.write(f"{c_e_garde} prduits C-E pour {category}\n")
                sys.stdout.write(f"{a_b_grade} produits A-B pour {category}\n")

                # and if there are no similar entries in the base
                if not Product.objects.filter(name=product['product_name'].lower()) and\
                    not Product.objects.filter(id=product['id']) and \
                    product['product_name'] is not '' and \
                    'test' not in product['product_name'].lower():

                    # test if product has a nutrition grade
                    if re.match('[a-b]', product['nutrition_grades']) and a_b_grade < 10:
                        a_b_grade += 1
                    elif re.match('[c-e]', product['nutrition_grades']) and c_e_garde < 10:
                        c_e_garde += 1
                    else:
                        sys.stdout.write(colored(f"Nous avons suffisament de produits avec une note {product['nutrition_grades']}\n\n", 'yellow'))
                        continue

                    sys.stdout.write(colored(f"{product['product_name']} id: {product['id']} ajouté en base\n\n", 'green'))

                    prod = Product(id=product['code'])

                    # testing and saving images URLs
                    if test_image_url(product['image_front_url']) and\
                        test_image_url(product['image_nutrition_url']):
                        prod.picture = product['image_front_url']
                        prod.nutrition = product['image_nutrition_url']
                    else:
                        continue

                    prod.nutriscore = product['nutrition_grades']
                    prod.name = product['product_name'].lower()
                    prod.summation = product['generic_name']
                    prod.external_link = f"https://fr.openfoodfacts.org/produit/{product['code']}/"
                    prod.save()

                    # getting product categories
                    category_level = len(product['categories_hierarchy'])
                    for cat in product['categories_hierarchy']:
                        label = cat.split(':')[-1]
                        label = label.replace('-', ' ')

                        try:
                            c = Category.objects.get(label=label)
                        except Category.DoesNotExist:
                            c = Category(label=label)
                            c.save()

                        Specificity(category=c, product=prod, level=category_level).save()
                        category_level -=1

                else:
                    sys.stdout.write(colored(f"{product['product_name']} id: {product['id']} DEJA en BASE \n\n", 'red'))
            else:
                for key in keys:
                    if key not in product:
                        try:
                            sys.stdout.write(colored(f"la clé {key} n'est pas dans {product['product_name']} id: {product['id']}\n\n", 'red'))
                        except KeyError:
                            sys.stderr.write(colored('pas de champs id\n\n', 'red'))
