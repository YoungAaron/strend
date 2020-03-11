from django.contrib import admin
from stock.models import *

@admin.register(StockList)
class StockListAdmin(admin.ModelAdmin):
    list_display  = ('id', 'ts_code', 'symbol', 'name', 'area', 'industry', 'fullname', 'list_status', 'list_date', 'is_hs')

@admin.register(IndexList)
class IndexListAdmin(admin.ModelAdmin):
    list_display = ('id', 'ts_code', 'name', 'market', 'publisher', 'index_type', 'category', 'base_date', 'base_point', 'list_date', 'weight_rule', 'fun_one', 'fun_two')

@admin.register(Repurchase)
class RepurchaseAdmin(admin.ModelAdmin):
    list_display = ('ts_code', 'ann_date', 'end_date', 'proc', 'exp_date', 'vol', 'amount', 'high_limit', 'low_limit')