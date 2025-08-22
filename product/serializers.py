from rest_framework import serializers
from .models import HalfProduct, ProductHalfProduct, Product


class HalfProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = HalfProduct
        fields = [
            "id", "name", "price", "type",
            "amount_of_qop", "kg",
            "description", "barn", "total_price", "total_kg"
        ]
        read_only_fields = ["total_price", "total_kg"]
        extra_kwargs = {
            "amount_of_qop": {"required": False, "allow_null": True},
            "kg": {"required": False, "allow_null": True},
        }

    def validate(self, data):
        type = data.get("type")

        if type == "kg":
            # faqat kg maydoni to'ldirilishi kerak
            if not data.get("kg"):
                raise serializers.ValidationError(
                    {"kg": "KG statusida 'kg' maydoni kiritilishi kerak"}
                )
            if data.get("amount_of_qop"):
                raise serializers.ValidationError(
                    {"detail": "KG statusida 'amount_of_qop' kiritilmasligi kerak"}
                )

        elif type == "qop":
            # qop tanlanganda qoplar soni va har bir qopdagi kg kiritilishi shart
            if not data.get("amount_of_qop") or not data.get("kg"):
                raise serializers.ValidationError(
                    {"detail": "QOP statusida 'amount_of_qop' va 'kg' kiritilishi kerak"}
                )

        return data

    def create(self, validated_data):
        type = validated_data.get("type")
        price = validated_data.get("price")

        if type == "kg":
            # umumiy kg bevosita kiritilgan
            total_kg = validated_data["kg"]
        else:
            # qop: umumiy kg = qop soni * har bir qopdagi kg
            total_kg = validated_data["amount_of_qop"] * validated_data["kg"]

        validated_data["total_kg"] = total_kg
        validated_data["total_price"] = price * total_kg

        return super().create(validated_data)


class HalfProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HalfProduct
        fields = [
            "id", "name", "price", "type",
            "amount_of_qop", "kg",
            "description", "barn"
        ]
        extra_kwargs = {
            "name": {"required": False},
            "price": {"required": False},
            "type": {"required": False},
            "amount_of_qop": {"required": False},
            "kg": {"required": False},
            "description": {"required": False},
            "barn": {"required": False},
        }

    def validate(self, data):
        type = data.get("type")

        if type == "kg":
            if not data.get("kg") and not self.instance:
                raise serializers.ValidationError(
                    {"kg": "KG statusida 'kg' maydoni kiritilishi kerak"}
                )
            if data.get("amount_of_qop"):
                raise serializers.ValidationError(
                    {"detail": "KG statusida 'amount_of_qop' kiritilmasligi kerak"}
                )

        elif type == "qop":
            amount_of_qop = data.get("amount_of_qop") or (self.instance.amount_of_qop if self.instance else None)
            kg = data.get("kg") or (self.instance.kg if self.instance else None)

            if not amount_of_qop or not kg:
                raise serializers.ValidationError(
                    {"detail": "QOP statusida 'amount_of_qop' va 'kg' kiritilishi kerak"}
                )

        return data

    def create(self, validated_data):
        type = validated_data.get("type")
        price = validated_data.get("price")

        if type == "kg":
            total_kg = validated_data["kg"]
        else:
            total_kg = validated_data["amount_of_qop"] * validated_data["kg"]

        validated_data["total_kg"] = total_kg
        validated_data["total_price"] = price * total_kg

        return super().create(validated_data)

    def update(self, instance, validated_data):
        type = validated_data.get("type", instance.type)
        price = validated_data.get("price", instance.price)

        if type == "kg":
            total_kg = validated_data.get("kg", instance.kg)
        else:
            amount_of_qop = validated_data.get("amount_of_qop", instance.amount_of_qop)
            kg = validated_data.get("kg", instance.kg)
            total_kg = amount_of_qop * kg

        validated_data["total_kg"] = total_kg
        validated_data["total_price"] = price * total_kg

        return super().update(instance, validated_data)



class ProductHalfProductNestedSerializer(serializers.ModelSerializer):
    half_product_id = serializers.PrimaryKeyRelatedField(
        queryset=HalfProduct.objects.all(),
        source="half_product"
    )

    class Meta:
        model = ProductHalfProduct
        fields = ["half_product_id", "used_kg"]
        # used_qops property sifatida hisoblanadi, shuning uchun field emas


class ProductCreateSerializer(serializers.ModelSerializer):
    half_products = ProductHalfProductNestedSerializer(
        many=True, write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id", "name", "price", "type", "amount_of_quti", "kg",
            "description", "half_products"
        ]
        extra_kwargs = {
            "amount_of_quti": {"required": False, "allow_null": True},
            "kg": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        half_products_data = validated_data.pop("half_products", [])
        product = Product.objects.create(**validated_data)

        for hp_data in half_products_data:
            ProductHalfProduct.objects.create(
                product=product,
                half_product=hp_data["half_product"],
                used_kg=hp_data.get("used_kg", 0)
            )

        product.update_totals()
        return product


class ProductListSerializer(serializers.ModelSerializer):
    half_products_detail = ProductHalfProductNestedSerializer(
        source="producthalfproduct_set", many=True, read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id", "name", "price", "type", "amount_of_quti", "kg",
            "description", "total_price", "total_kg", "created_at",
            "half_products_detail"
        ]
        read_only_fields = ["total_price", "total_kg", "half_products_detail"]