from django.db import models


# Mahsulot jadvali (Ko'ylak, shim)
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)