from rest_framework import serializers

from .models import Diller


class DillerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diller
        fields = ['id', 'name', 'location', 'description', 'phone_number']
