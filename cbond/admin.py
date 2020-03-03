from django.contrib import admin
from cbond.models import *


@admin.register(CbondList)
class CbondListAdmin(admin.ModelAdmin):
    list_display  = ('ts_code', 'bond_full_name', 'stk_code', 'stk_short_name', 'maturity', 'issue_price', 'issue_size', 'list_date', 'conv_start_date', 'first_conv_price')