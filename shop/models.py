from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=500, unique=True)
    location = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=40, unique=True, null=False)
    description = models.TextField()

    def __str__(self):
        return self.name
