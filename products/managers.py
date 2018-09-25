# -*- coding: utf-8 -*

from django.db import models
from products.models import Product
from django.db.models import Q

#MANAGERS
class ProductManager(models.Manager):

    def six_better_products(self, product):

        #list of the 6 returned products
        returned_products = []
        #list of existing nutriscores
        scores = ['a','b','c','d','e']
        #We start with the most stecific category of the product
        category_rank = 1


        #i start searching products with 'a' grade
        for score in scores:
            print(f'score {score}')
            for cat_specificities in product.specificity_set.all().order_by('level'):
            # if returned_products is not full and
            # we are not looking for a worst nutriscore$
                if len(returned_products) < 6 and score < product.nutriscore and cat_specificities.level < 4:

                    products = Product.objects.filter(Q(categories__label=cat_specificities.category)\
                                                    & Q(nutriscore = score))
                    # i look for products with an inferior nutrition grade
                    for prod in products:
                        if len(returned_products) < 6 and prod not in returned_products:
                            returned_products.append(prod)
                        else:
                            break

        if len(returned_products) == 6:
            return returned_products
        else:
            return False