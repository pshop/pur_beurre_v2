from django.db import models
from users.models import CustomUser
from products.management.local_search import ProductManager

class Category(models.Model):

    label = models.CharField(max_length=150, unique=True)

    class meta:
        verbose_name = 'categorie'

    def __str__(self):
        return self.label


class Product(models.Model):

    id = models.IntegerField(primary_key=True)
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

    class meta:
        verbose_name = 'product'

    def __str__(self):
        return self.name


class Specificity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.IntegerField()

    def __str__(self):
        return str(self.level)