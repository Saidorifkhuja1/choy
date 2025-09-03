from rest_framework import serializers
from decimal import Decimal, InvalidOperation
from .models import SoldProduct


class SoldProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldProduct
        fields = "__all__"
        read_only_fields = ["id", "total_price", "debt", "created_at"]


class SoldProductCreateSerializer(serializers.ModelSerializer):
    # CharField qilib olamiz, keyin validate() ichida Decimal ga o‘tkazamiz
    quti = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="0")
    kg = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="0")

    class Meta:
        model = SoldProduct
        fields = [
            "id",
            "name",
            "dealer",
            "product",
            "quti",
            "kg",
            "price",
            "total_price",
            "paid_price",
            "debt",
            "created_at",
        ]
        read_only_fields = ["id", "total_price", "debt", "created_at"]

    def validate(self, attrs):
        # Quti ni son qilib o‘tkazamiz
        try:
            quti = int(attrs.get("quti") or 0)
        except (ValueError, TypeError):
            quti = 0

        # Kg ni decimal qilib o‘tkazamiz
        try:
            kg = Decimal(attrs.get("kg") or "0")
        except (InvalidOperation, TypeError, ValueError):
            kg = Decimal("0.00")

        # Ikkalasi ham 0 bo‘lsa – xato
        if quti == 0 and kg == 0:
            raise serializers.ValidationError("❌ Quti yoki Kg dan bittasi kiritilishi shart")

        attrs["quti"] = quti
        attrs["kg"] = kg

        return attrs

    def create(self, validated_data):
        return SoldProduct.objects.create(**validated_data)