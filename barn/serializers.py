from rest_framework import serializers


from .models import Barn


class BarnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barn
        fields = ['id', 'name', 'location', 'description', 'phone_number']