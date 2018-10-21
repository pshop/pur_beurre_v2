from django.test import TestCase
from products.openfoodapi import OpenFoodAPI



class IndexTests(TestCase):

    test_product = {
        'id': "123",
        'nutrition_grades': "a",
        'product_name': "nametest",
        'generic_name': "gen_name",
        'image_front_url': "URL IMAGE",
        'image_nutrition_url': "url nutri",
        'url': "url",
        'categories_hierarchy': [
            'cat1',
            'cat2',
            'cat3'
        ],
    }
    def test_dict_has_required_key(self):

        self.assertTrue(OpenFoodAPI().check_has_needed_infos(self.test_product))

    def test_dict_has_NOT_required_key(self):
        self.assertFalse(OpenFoodAPI().check_has_needed_infos({}))

    def test_add_full_product_in_base(self):
        pass

    def test_add_product_name_missing(self):
        pass

    def test_add_product_nutriscore_missing(self):
        pass

    def test_search_product_not_in_base(self):
        pass

    def test_search_product_in_base(self):
        pass

    def test_cleaning_api_infos(self):
        pass

    def test_saving_product(self):
        pass

    def test_already_saved_product(self):
        pass