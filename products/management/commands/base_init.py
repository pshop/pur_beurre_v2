from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from products.management.commands._open_food_facts import OpenFoodFacts
from products.models import Category


class Command(BaseCommand):
    """
    get all nutella categories and add to the base 100
    products related to these categories
    """

    def handle(self, *args, **options):

        _ = OpenFoodFacts()

        for category in _.get_nutella_categories():
            try:
                cat = Category(label=category)
                cat.save()
            except IntegrityError as e:
                CommandError(f"{category} is already in base")

        self.stdout.write(self.style.SUCCESS(len(_.get_products_by_category('breakfasts'))))



