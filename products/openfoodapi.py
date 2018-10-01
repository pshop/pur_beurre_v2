import openfoodfacts
import json

class OpenFoodAPI():

    def __init__(self):
        pass

    def search_product(self, search_term):

        #if search for a product with the basic search
        #of the openfoodfact api
        search_result = openfoodfacts.products.search(search_term)
        #if i find 1 or more products
        if search_result['count'] > 0:
            #i return the first product
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

        try:
            cleaned_prod = {
                'id': prod['code'],
                'nutriscore': prod['nutrition_grades'],
                'name': prod['product_name'],
                'summation': prod['generic_name'],
                'picture': prod['image_front_url'],
                'nutrition': prod['image_nutrition_url'],
                'external_link': prod['url'],
                'categories': prod['categories_tags'],
            }
            return cleaned_prod
        except:
            return False

    def return_six_healthy_prods(self, search_term):

        # i take the result of the search
        initial_product = self.search_product(search_term)
        categories_list = []
        healthy_products_list = []
        nutriscores = ['a', 'b', 'c', 'd', 'e']


        #if a have a result
        if initial_product:
            #i take the categories in hierachy's reversed order
            # and put all that in a list
            for cat in reversed(initial_product['categories_hierarchy']):
                cat_name = cat.split(':')[-1]
                categories_list.append(cat_name.replace('-', ' '))

            for cat in categories_list:
                for score in nutriscores:
                    for prod in self.search_by_cat_and_score(score, cat):
                        cleaned_prod = self.clean_prod_info(prod)
                        if cleaned_prod:
                            healthy_products_list.append(cleaned_prod)
                        if len(healthy_products_list) > 5:
                            break
                    if len(healthy_products_list) > 5:
                        break
                if len(healthy_products_list) > 5:
                    break

            return healthy_products_list

        # if not result return false
        else:
            return False


if __name__ == '__main__':

    open_food_api = OpenFoodAPI()

    results = open_food_api.return_six_healthy_prods('nutella')
    for prod in results:
        print(prod)