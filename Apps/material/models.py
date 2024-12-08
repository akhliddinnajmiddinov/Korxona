from django.db import models


# Xomashyo jadvali (Mato, Ip, Tugma)
class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)