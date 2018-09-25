# -*- coding: utf-8 -*

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from products.management.commands._open_food_facts import OpenFoodFacts
from products.models import Category, Product


class Command(BaseCommand):
    """
    get all nutella categories and add to the base 100
    products related to these categories
    """

    def handle(self, *args, **options):

        _ = OpenFoodFacts()

        Category.objects.all().delete()
        for category in _.get_nutella_categories():
            try:
                cat = Category(label=category)
                cat.save()
            except IntegrityError as e:
                CommandError(f"{category} is already in base")


        categories = Category.objects.values_list('label', flat=True)

        for cat in categories:
            _.get_products_by_category(cat)