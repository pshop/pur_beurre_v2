from django.test import TestCase

from products.openfoodapi import OpenFoodAPI
from products.management.commands import _open_food_facts as off
from products.models import Product, Category
from users.models import CustomUser
import logging
log = logging.getLogger(__name__)


class IndexTests(TestCase):

    def setUp(self):
        self.test_product = {
            'id': '123',
            'nutrition_grades': "a",
            'product_name': "product nametest",
            'generic_name': "gen_name description",
            'image_front_url': "URL IMAGE",
            'image_nutrition_url': "url nutri",
            'url': "url",
            'categories_hierarchy': [
                'cat1',
                'cat2',
                'cat3'
            ],
        }

        CustomUser(first_name='first name test',
                   email='test@test.fr',
                   password='test').save()

        Product(
            id=self.test_product['id'],
            nutriscore=self.test_product['nutrition_grades'],
            name=self.test_product['product_name'],
            summation=self.test_product['generic_name'],
            picture=self.test_product['image_front_url'],
            nutrition=self.test_product['image_nutrition_url'],
            external_link=self.test_product['url']
        ).save()

    def test_dict_has_required_key(self):
        self.assertTrue(OpenFoodAPI().check_has_needed_infos(self.test_product))

    def test_dict_has_NOT_required_key(self):
        self.assertFalse(OpenFoodAPI().check_has_needed_infos({}))

    def test_test_image_url_with_valid_URL(self):
        self.assertTrue(off.test_image_url("https://static.openfoodfacts.org/images/products/301/762/042/9484/nutrition_fr.106.400.jpg"))

    def test_test_image_url_with_NOT_valid_URL(self):
        self.assertFalse(off.test_image_url(
            "https://static.openfoodfacts.org/images/products/301/762/042/94"))

    def test_add_product(self):
        prod = Product(
            id=self.test_product['id'],
            nutriscore=self.test_product['nutrition_grades'],
            name=self.test_product['product_name'],
            summation=self.test_product['generic_name'],
            picture=self.test_product['image_front_url'],
            nutrition=self.test_product['image_nutrition_url'],
            external_link=self.test_product['url']
        )
        prod.save()
        prod = Product.objects.get(id=self.test_product['id'])
        self.assertTrue(prod)

    def test_add_product_to_fav(self):
        user = CustomUser.objects.get(first_name='first name test')
        user.products.add(Product.objects.get(id='123'))

        self.assertEqual(user.products.get(id="123"), Product.objects.get(id='123'))


