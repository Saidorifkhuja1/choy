
from rest_framework import serializers
from .models import SoldProduct

class SoldProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldProduct
        fields = ["id", "name", "price", "kg", "quti", "total_price", "paid_price", "debt", "created_at"]
        read_only_fields = ["total_price", "debt"]  # avtomatik hisoblanadi

    def create(self, validated_data):
        # price ni olib olish
        price = validated_data.get("price", 0)
        kg = validated_data.get("kg", 0)
        quti = validated_data.get("quti", 0)

        # total_price hisoblash
        if kg and kg > 0:
            total_price = price * kg
        elif quti and quti > 0:
            total_price = price * quti
        else:
            total_price = 0

        validated_data["total_price"] = total_price

        # debt hisoblash
        paid_price = validated_data.get("paid_price", 0)
        validated_data["debt"] = total_price - paid_price

        return super().create(validated_data)

