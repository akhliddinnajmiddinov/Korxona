from django.db import models


# Xomashyo jadvali (Mato, Ip, Tugma)
class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def save(self):
        self.name = self.name.lower()
        super().save()

    def __str__(self):
        return self.name