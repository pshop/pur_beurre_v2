from django.db import models
from django.db.models import Q
from users.models import CustomUser

import logging

log = logging.getLogger(__name__)

# MANAGERS


class ProductManager(models.Manager):

    def six_better_products(self, product):

        # ist of the 6 returned products
        returned_products = []
        # list of existing nutriscores
        scores = ['a', 'b', 'c', 'd', 'e']

        # i start searching products with 'a' grade
        for score in scores:
            for cat_specificities in product.specificity_set.all().order_by('level'):
                # if returned_products is not full and
                # we are not looking for a worst nutriscore$
                if len(returned_products) < 6 and score < product.nutriscore and cat_specificities.level < 4:

                    products = Product.objects.filter(Q(categories__label=cat_specificities.category) &
                                                      Q(nutriscore=score))
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



# MODELS


class Category(models.Model):

    label = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'categorie'

    def __str__(self):
        return self.label


class Product(models.Model):

    id = models.BigIntegerField(primary_key=True)
    user = models.ManyToManyField(
        CustomUser,
        related_name='products'
    )
    nutriscore = models.CharField(max_length=1)
    name = models.CharField(max_length=150, unique=True)
    summation = models.CharField(max_length=300)
    picture = models.URLField()
    nutrition = models.URLField()
    external_link = models.URLField()
    objects = ProductManager()
    categories = models.ManyToManyField(
        Category,
        through='Specificity',
        related_name='products'
    )

    class Meta:
        verbose_name = 'product'

    def __str__(self):
        return self.name


class Specificity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.IntegerField()

    def __str__(self):
        return str(self.level)
