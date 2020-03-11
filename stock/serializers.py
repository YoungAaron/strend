from rest_framework import serializers
from stock.models import *


class RepurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repurchase
        fields = '__all__'

class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexList
        fields = '__all__'