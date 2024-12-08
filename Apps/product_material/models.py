from django.db import models
from product.models import Product
from material.models import Material


# Mahsulot-Xomashyo yordamchi jadvali
class Product_Materials(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()