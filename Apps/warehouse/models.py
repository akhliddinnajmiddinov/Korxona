from django.db import models
from material.models import Material

# Omborxona jadvali
class Warehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.FloatField()
    price = models.IntegerField()

    def __str__(self):
        return f'{self.material.name} & {self.remainder} : {self.price}$'