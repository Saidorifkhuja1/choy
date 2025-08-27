from decimal import Decimal
from django.db import models

from diller.models import Diller
from product.models import Product


class SoldProduct(models.Model):
    name = models.CharField(max_length=1000)
    dealer = models.ForeignKey(Diller, on_delete=models.CASCADE, related_name="sold_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sold_products")

    quti = models.PositiveIntegerField(null=True, blank=True)  # agar type=quti bo‘lsa
    kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # agar type=kg bo‘lsa

    # sotuv narxi (product.price dan default olish mumkin)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # avtomatik hisoblanadi

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Default price ni product.price bilan to‘ldirish
        if not self.price:
            self.price = self.product.price

        # Umumiy narxni hisoblash
        if self.product.type == "quti" and self.quantity_quti:
            self.total_price = Decimal(self.quantity_quti) * self.price
        elif self.product.type == "kg" and self.quantity_kg:
            self.total_price = Decimal(self.quantity_kg) * self.price

        # Qarzdorlikni hisoblash
        self.debt = self.total_price - self.paid_price

        # Ombordagi product miqdorini kamaytirish (faqat yangi yozuv yaratilganda)
        if self.pk is None:
            if self.product.type == "quti" and self.quantity_quti:
                if self.product.amount_of_quti < self.quantity_quti:
                    raise ValueError("Omborda yetarli quti mavjud emas")
                self.product.amount_of_quti -= self.quantity_quti
                self.product.save()
            elif self.product.type == "kg" and self.quantity_kg:
                if self.product.kg < self.quantity_kg:
                    raise ValueError("Omborda yetarli kg mavjud emas")
                self.product.kg -= self.quantity_kg
                self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dealer.name} - {self.product.name} ({self.total_price})"