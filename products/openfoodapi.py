import openfoodfacts
import logging

from itertools import product as cartesian_product

log = logging.getLogger(__name__)

class OpenFoodAPI():

    def __init__(self):
        pass

    def search_product(self, search_term):

        # if search for a product with the basic search
        # of the openfoodfact api
        # TODO add limit to search
        search_result = openfoodfacts.products.search(search_term)
        # if i find 1 or more products
        if search_result['count'] > 0:
            # i return the first product
            return search_result['products'][0]
        else:
            return False

    def search_by_cat_and_score(self, nutriscore, category):

        products_list = []

        search_result = openfoodfacts.products.advanced_search({
            "search_terms": "",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "tagtype_1": 'nutrition_grades',
            "tag_contains_1": 'contains',
            "tag_1": nutriscore,
            "sort_by": 'unique_scans_n',
            "page_size": "20",
            "json": 1
        })

        return search_result['products']

    def clean_prod_info(self, prod):

        cleaned_prod = {
            'id': prod.get('code', '0'),
            'nutriscore': prod.get('nutrition_grades', 'e'),
            'name': prod.get('product_name', 'nameless'),
            'summation': prod.get('generic_name', 'pas de descritpion'),
            'picture': prod.get('image_front_url', 'no image'),
            'nutrition': prod.get('image_nutrition_url'),
            'external_link': f"https://fr.openfoodfacts.org/produit/{prod.get('code', '0')}/",
            'categories': prod.get('categories_tags'),
        }
        return cleaned_prod

    def check_has_needed_infos(self, prod):
        keys = ('id',
                'nutrition_grades',
                'product_name',
                'generic_name',
                'image_front_url',
                'image_nutrition_url',
                'url',
                'categories_hierarchy',
                )
        if all(key in prod for key in keys):
            return True
        else:
            return False

    def return_six_healthy_prods(self, search_term):

        # i take the result of the search
        initial_product = self.search_product(search_term)
        categories_list = []
        healthy_products_list = []
        nutriscores = ['a', 'b', 'c']


        #if a have a result
        if initial_product:
            #i take the categories in hierachy's reversed order
            # and put all that in a list
            for category in reversed(initial_product['categories_hierarchy']):
                cat_name = category.split(':')[-1]
                categories_list.append(cat_name.replace('-', ' '))

            for score, category in cartesian_product(nutriscores, categories_list):

                for product in self.search_by_cat_and_score(score, category):
                    if self.check_has_needed_infos(product):
                        cleaned_prod = self.clean_prod_info(product)

                        if cleaned_prod:
                            healthy_products_list.append(cleaned_prod)
                        if len(healthy_products_list) > 5:
                            break

                if len(healthy_products_list) > 5:
                    break

            return healthy_products_list

        # if not result return false
        else:
            return []


if __name__ == '__main__':

    open_food_api = OpenFoodAPI()

    results = open_food_api.return_six_healthy_prods('nutella')
    for prod in results:
        print(prod)