from django.db import models
from users.models import CustomUser

# Create your models here.
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
    categories = models.ManyToManyField(
        Category,
        related_name='products'
    )

    class meta:
        verbose_name = 'product'

    def __str__(self):
        return self.name

