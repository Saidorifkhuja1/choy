from django.db import models

from barn.models import Barn


from django.db import models
from barn.models import Barn

class HalfProduct(models.Model):
    TYPE_CHOICES = (
        ("kg", "Kg"),
        ("qop", "Qop"),
    )

    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount_of_qop = models.PositiveIntegerField( null=True, blank=True)
    kg = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    barn = models.ForeignKey(Barn, on_delete=models.CASCADE)
    total_kg = models.PositiveIntegerField( default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name



# class Product(models.Model):
#     TYPE_CHOICES = (
#         ("kg", "Kg"),
#         ("quti", "Quti"),)
#     name = models.CharField(max_length=1000)
#     half_product = models.ForeignKey(HalfProduct, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES)
#     amount_of_quti = models.PositiveIntegerField( default=0)
#     kg = models.PositiveIntegerField(null=True, blank=True)
#     description = models.TextField( null=True, blank=True)
#     total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     total_kg = models.PositiveIntegerField( default=0)
#
#