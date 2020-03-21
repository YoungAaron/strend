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

class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockList
        fields = '__all__'

class HolderTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolderTrade
        fields = '__all__'

class HolderNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolderNumber
        fields = '__all__'

class TraderAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraderAccount
        fields = '__all__'

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'

class ExpressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Express
        fields = '__all__'

class MarginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Margin
        fields = '__all__'

class FundListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundList
        fields = '__all__'

class FundPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundPortfolio
        fields = '__all__'