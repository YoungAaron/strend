from django.contrib import admin
from stock.models import *

@admin.register(StockList)
class StockListAdmin(admin.ModelAdmin):
    list_display  = ('id', 'ts_code', 'symbol', 'name', 'area', 'industry', 'fullname', 'list_status', 'list_date', 'is_hs')

@admin.register(IndexList)
class IndexListAdmin(admin.ModelAdmin):
    list_display = ('id', 'ts_code', 'name', 'market', 'publisher', 'index_type', 'category', 'base_date', 'base_point', 'list_date', 'weight_rule', 'select_opt')

@admin.register(Repurchase)
class RepurchaseAdmin(admin.ModelAdmin):
    list_display = ('ts_code', 'ann_date', 'end_date', 'proc', 'exp_date', 'vol', 'amount', 'high_limit', 'low_limit')

@admin.register(HolderTrade)
class HolderTradeAdmin(admin.ModelAdmin):
    list_display = ('ts_code', 'ann_date', 'holder_name', 'holder_type', 'in_de', 'change_vol', 'change_ratio', 'after_share', 'after_ratio', 'avg_price', 'begin_date', 'close_date')

@admin.register(Express)
class ExpressAdmin(admin.ModelAdmin):
    list_display = ('ts_code', 'ann_date', 'end_date', 'revenue', 'operate_profit', 'n_income')

@admin.register(HolderNumber)
class HolderNumberAdmin(admin.ModelAdmin):
    list_display = ('ts_code', 'ann_date', 'end_date', 'holder_num')

@admin.register(TraderAccount)
class TraderAccountAdmin(admin.ModelAdmin):
    list_display = ('date', 'weekly_new', 'total', 'weekly_hold', 'weekly_trade')

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('ts_code', 'ann_date', 'end_date', 'report_type', 'comp_type', 'total_revenue', 'total_profit', 'n_income')

@admin.register(FundList)
class FundListAdmin(admin.ModelAdmin):
    list_display = ('ts_code', 'name', 'management', 'fund_type', 'found_date', 'due_date', 'list_date', 'delist_date', 'issue_amount', 'exp_return', 'status', 'invest_type')

@admin.register(FundPortfolio)
class FundPortfolioAdmin(admin.ModelAdmin):
    list_display = ('ts_code', 'ann_date', 'end_date', 'symbol', 'mkv', 'amount', 'stk_mkv_ratio', 'stk_float_ratio')

@admin.register(ShareFloat)
class ShareFloatAdmin(admin.ModelAdmin):
    list_display = ('ts_code', 'ann_date', 'float_date', 'float_share', 'float_ratio', 'holder_name', 'share_type')

@admin.register(PledgeStat)
class PledgeStatAdmin(admin.ModelAdmin):
    list_display = ('ts_code', 'end_date', 'pledge_count', 'unrest_pledge', 'rest_pledge', 'total_share', 'pledge_ratio')

@admin.register(Margin)
class MarginAdmin(admin.ModelAdmin):
    list_display = ('trade_date', 'exchange_id', 'rzye', 'rzmre', 'rqye', 'rzrqye', 'rqyl')
