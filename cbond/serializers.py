from rest_framework import serializers
from cbond.models import *


class CbondListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CbondList
        fields = '__all__'