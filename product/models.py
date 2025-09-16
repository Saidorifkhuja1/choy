from django.db import models
from barn.models import Barn
from decimal import Decimal
from rest_framework import serializers



class HalfProduct(models.Model):
    TYPE_CHOICES = (
        ("kg", "Kg"),
        ("qop", "Qop"),
    )
    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount_of_qop = models.DecimalField(max_digits=10,decimal_places=1, null=True,blank=True)
    kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    barn = models.ForeignKey(Barn, on_delete=models.CASCADE)
    total_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    @property
    def available_kg(self):
        """Mavjud kg miqdorini qaytaradi"""
        if self.type == "kg":
            return float(self.total_kg)
        elif self.type == "qop" and self.kg and self.amount_of_qop:
            return float(self.amount_of_qop) * float(self.kg)
        return 0

    def has_sufficient_stock(self, required_kg):
        """Yetarli zaxira borligini tekshiradi"""
        return self.available_kg >= required_kg



class Product(models.Model):
    TYPE_CHOICES = (
        ("kg", "Kg"),
        ("quti", "Quti"),
    )

    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount_of_quti = models.PositiveIntegerField(default=0, null=True, blank=True)
    kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # ManyToMany HalfProduct through ProductHalfProduct
    half_products = models.ManyToManyField(
        HalfProduct,
        through="ProductHalfProduct",
        related_name="products"
    )

    def __str__(self):
        return self.name

    def calculate_total_cost(self):
        """Productning umumiy tannarxini hisoblaydi"""
        return sum(php.calculate_cost() for php in self.producthalfproduct_set.all())

    def calculate_total_kg(self):
        """Product umumiy kg hisoblaydi"""
        total = Decimal('0.00')
        for php in self.producthalfproduct_set.all().select_related("half_product"):
            if php.half_product.type == "kg":
                total += php.used_kg
            elif php.half_product.type == "qop" and php.half_product.kg:
                total += Decimal(str(php.used_qops)) * php.half_product.kg
        return total

    def update_totals(self):
        """Total price va total kg avtomatik yangilash"""
        self.total_kg = self.calculate_total_kg()

        if self.type == "quti":  # ✅ agar quti bo'lsa
            self.total_price = self.price * Decimal(str(self.amount_of_quti or 0))
        else:  # ✅ kg bo'lsa
            self.total_price = self.price * self.total_kg

        self.save(update_fields=["total_price", "total_kg"])


class ProductHalfProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="producthalfproduct_set")
    half_product = models.ForeignKey(HalfProduct, on_delete=models.CASCADE, related_name="producthalfproduct_set")
    used_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ("product", "half_product")
        verbose_name = "Product HalfProduct"
        verbose_name_plural = "Product HalfProducts"

    def __str__(self):
        return f"{self.product.name} <- {self.half_product.name} ({self.used_kg} kg)"

    @property
    def used_qops(self):
        """Ishlatilgan qoplar sonini hisoblaydi (kasr sonlarda ham)"""
        if self.half_product.type == "qop" and self.half_product.kg:
            return float(self.used_kg) / float(self.half_product.kg)
        return 0

    def clean(self):
        """Validatsiya: yetarli zaxira borligini tekshirish"""
        if self.half_product and not self.half_product.has_sufficient_stock(float(self.used_kg)):
            raise serializers.ValidationError({
                "used_kg": (
                    f"'{self.half_product.name}' uchun zaxira yetarli emas. "
                    f"Mavjud: {self.half_product.available_kg} kg, "
                    f"Talab: {self.used_kg} kg"
                )
            })

    def calculate_cost(self):
        """Bog‘langan yarim mahsulot narxini hisoblaydi"""
        return self.used_kg * self.half_product.price

    def _update_half_product_stock(self, multiplier=1):
        """HalfProduct zaxiralarini yangilash"""
        kg_change = multiplier * float(self.used_kg)

        if self.half_product.type == "kg":

            self.half_product.kg = max(0, float(self.half_product.kg) - kg_change)
            self.half_product.total_kg = max(0, float(self.half_product.total_kg) - kg_change)

        elif self.half_product.type == "qop":
            used_qops = self.used_qops
            qop_change = multiplier * used_qops

            if self.half_product.amount_of_qop is not None:
                self.half_product.amount_of_qop = float(self.half_product.amount_of_qop) - qop_change


            self.half_product.kg = max(0, float(self.half_product.kg) - kg_change)
            self.half_product.total_kg = max(0, float(self.half_product.total_kg) - kg_change)


        self.half_product.total_price = Decimal(str(self.half_product.total_kg)) * self.half_product.price

        self.half_product.save(update_fields=['kg', 'total_kg', 'total_price', 'amount_of_qop'])

    def save(self, *args, **kwargs):
        """Saqlanganda validatsiya va zaxiralarni yangilash"""
        self.full_clean()
        if self.pk:
            old_instance = ProductHalfProduct.objects.get(pk=self.pk)
            old_instance._update_half_product_stock(multiplier=-1)
        super().save(*args, **kwargs)
        self._update_half_product_stock(multiplier=1)
        self.product.update_totals()

    def delete(self, *args, **kwargs):
        """O‘chirishda faqat Product totals yangilanadi"""
        product = self.product
        super().delete(*args, **kwargs)
        product.update_totals()





