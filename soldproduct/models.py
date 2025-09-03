from decimal import Decimal
from django.db import models

from diller.models import Diller
from product.models import Product


class SoldProduct(models.Model):
    name = models.CharField(max_length=1000)
    dealer = models.ForeignKey(Diller, on_delete=models.CASCADE, related_name="sold_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sold_products")

    quti = models.PositiveIntegerField(null=True, blank=True)
    kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Default price ni product.price bilan to‘ldirish
        if not self.price:
            self.price = self.product.price

        # Umumiy narxni hisoblash
        if self.product.type == "quti" and self.quti:
            self.total_price = Decimal(self.quti) * self.price
        elif self.product.type == "kg" and self.kg:
            self.total_price = Decimal(self.kg) * self.price

        # Qarzdorlikni hisoblash
        self.debt = self.total_price - self.paid_price

        # Ombordagi product miqdorini kamaytirish (faqat yangi yozuv yaratilganda)
        if self.pk is None:
            if self.product.type == "quti" and self.quti:
                if self.product.amount_of_quti < self.quti:
                    raise ValueError("❌ Omborda yetarli quti mavjud emas")
                self.product.amount_of_quti -= self.quti

                # Qolgan miqdordan total_kg ni kamaytirish
                if self.product.kg:
                    self.product.total_kg = max(
                        Decimal("0.00"),
                        self.product.total_kg - (Decimal(self.quti) * self.product.kg)
                    )

            elif self.product.type == "kg" and self.kg:
                if self.product.kg < self.kg:
                    raise ValueError("❌ Omborda yetarli kg mavjud emas")
                self.product.kg -= self.kg
                self.product.total_kg = max(Decimal("0.00"), self.product.total_kg - self.kg)

            # ✅ Product.total_price qayta hisoblash
            if self.product.type == "quti":
                self.product.total_price = Decimal(self.product.amount_of_quti) * self.product.price
            elif self.product.type == "kg":
                self.product.total_price = Decimal(self.product.kg) * self.product.price

            # Product ni saqlash
            self.product.save(update_fields=["amount_of_quti", "kg", "total_kg", "total_price"])

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dealer.name} - {self.product.name} ({self.total_price})"


