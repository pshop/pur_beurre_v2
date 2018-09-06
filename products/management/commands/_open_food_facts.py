import openfoodfacts
import requests
import urllib.request
import re

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from products.models import Product

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
            cat_list.append(cat.split(':')[-1])

        return cat_list

    def get_products_by_category(self, category):

        search_result = openfoodfacts.products.advanced_search({
            "search_terms":"",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "sort_by": "unique_scans",
            "page_size": "100",
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
        products_list = []

        for product in search_result['products']:

            # if i got enough products i break the for loop
            if a_b_grade > 10 and c_e_garde > 10:
                break

            # i check if the product has all the needed keys
            if all(key in product for key in keys):

                # test if product has a nutrition grade
                if re.match('[a-b]', product['nutrition_grades']) and a_b_grade < 10:
                    a_b_grade += 1
                elif re.match('[c-e]', product['nutrition_grades']) and c_e_garde < 10:
                    c_e_garde += 1
                else:
                    continue

                # and if there are no similar entries in the base
                if not Product.objects.filter(name=product['product_name']) and\
                    not Product.objects.filter(id=product['id']):

                    product_infos = {}

                    # downloading products pictures
                    urllib.request.urlretrieve(product['image_front_url'], f"media/pictures/{product['id']}.jpg")

                    # downloading nutrition picture
                    urllib.request.urlretrieve(product['image_nutrition_url'], f"media/nutrition/{product['id']}.jpg")

                    # getting product categories
                    categories = []
                    for cat in product['categories_tags']:
                        categories.append(cat.split(':')[-1])

                    product_infos['id'] = product['code']
                    product_infos['nutriscore'] = product['nutrition_grades']
                    product_infos['name'] = product['product_name']
                    product_infos['summation'] = product['generic_name']
                    product_infos['external_link'] = product['url']
                    product_infos['categories'] = categories

                    products_list.append(product_infos)

            else:
                continue

        return products_list


if __name__ == '__main__':

    _ = OpenFoodFacts()

    print(_.get_products_by_category('breakfasts'))
