from django.db import models
from users.models import CustomUser

# Create your models here.
class Category(models.Model):
    label = models.CharField(max_length=150)

class Product(models.Model):
    user = models.ManyToManyField(CustomUser)
    nutriscore = models.CharField(max_length=1)
    name = models.CharField(max_length=150)
    picture = models.ImageField(upload_to='images/pictures/')
    nutrition = models.ImageField(upload_to='images/nutrition/')
    external_link = models.URLField()
    categories = models.ManyToManyField(
        Category,
        related_name='products'
    )