# -*- coding: utf-8 -*

from products.models import Product
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'returns categories of the given product ordered by specificity indice'

    def add_arguments(self, parser):
        parser.add_argument('product', nargs='+', type=str)

    def handle(self, *args, **options):

        prod = options['product'][0]
        try:
            prod = Product.objects.get(name=prod)
        except:
            raise CommandError(f"{prod} n'existe pas dans la base")

        for spec in prod.specificity_set.all():
            print(spec.product.name)
            print(spec.level)
            print(spec.category.label)

