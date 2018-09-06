import openfoodfacts
import requests
import urllib.request
import re
import sys
from termcolor import colored

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import IntegrityError
from django.core.management.base import CommandError

from products.models import Product, Category

def save_image_from_url(model, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    model.picture.save("image.jpg", File(img_temp), save=True)

class OpenFoodFacts():

    def get_nutella_categories(self):

        result = openfoodfacts.products.advanced_search({
            "search_terms":'nutella',
            "page_size": "1",
        })

        cat_list = []

        for cat in result['products'][0]['categories_tags']:
            cat_name = cat.split(':')[-1]
            cat_list.append(cat_name.replace('-', ' '))

        return cat_list

    def get_products_by_category(self, category):

        search_result = openfoodfacts.products.advanced_search({
            "search_terms":"",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "sort_by": "unique_scans",
            "page_size": "200",
            "json":"1,"
        })

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
                'categories_tags',
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
                if not Product.objects.filter(name=product['product_name']) and\
                    not Product.objects.filter(id=product['id']):

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

                    # downloading products pictures
                    try:
                        urllib.request.urlretrieve(product['image_front_url'], f"media/pictures/{product['id']}.jpg")
                    except:
                        sys.stdout.write(colored("Image inaccessible\n\n","red"))
                        continue
                    prod.picture = File(open(f"media/pictures/{product['id']}.jpg", "rb"))

                    # downloading nutrition picture
                    try:
                        urllib.request.urlretrieve(product['image_nutrition_url'], f"media/nutrition/{product['id']}.jpg")
                    except:
                        sys.stdout.write(colored("Image inaccessible\n\n", "red"))
                        continue
                    prod.nutrition = File(open(f"media/nutrition/{product['id']}.jpg", "rb"))

                    prod.nutriscore = product['nutrition_grades']
                    prod.name = product['product_name']
                    prod.summation = product['generic_name']
                    prod.external_link = product['url']
                    prod.save()

                    # getting product categories
                    for cat in product['categories_tags']:
                        label = cat.split(':')[-1]
                        label = label.replace('-', ' ')

                        try:
                            c = Category.objects.get(label=label)
                        except Category.DoesNotExist:
                            c = Category(label=label)
                            c.save()

                        prod.categories.add(c)
                        prod.save()

                else:
                    sys.stdout.write(colored(f"{product['product_name']} id: {product['id']} DEJA en BASE \n\n", 'red'))
            else:
                for key in keys:
                    if key not in product:
                        try:
                            sys.stdout.write(colored(f"la clé {key} n'est pas dans {product['product_name']} id: {product['id']}\n\n", 'red'))
                        except KeyError:
                            sys.stderr.write(colored('pas de champs id\n\n', 'red'))


if __name__ == '__main__':

    _ = OpenFoodFacts()

    print(_.get_products_by_category('breakfasts'))
