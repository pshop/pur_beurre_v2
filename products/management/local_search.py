from django.db import models

class ProductManager(models.Manager):

    def six_better_products(self, product_id):
        pass
        #je prends mon produit

            #je récupère sa catégorie la plus spécifique
            #je cherche des produits de note a - b dans cette catégorie
            #je les implémente dans mon tableau de réponse
            #je vérifie que j'ai 6 produits,

                #si oui je revoie le tableau

                #si non je recommence avec une catégorie moins spécifique