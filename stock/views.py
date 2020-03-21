from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from stock.models import *
from stock.serializers import *

import tushare
pro = tushare.pro_api('60e379652b074a917985f88b293b702f3873c9767006d60e4d7b0875')
import time, datetime


# 股东回购视图
class RepurchaseListView(generics.ListCreateAPIView):
    queryset = Repurchase.objects.all()
    serializer_class = RepurchaseSerializer
    filterset_fields = ('ann_date', 'amount')

class RepurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repurchase.objects.all()
    serializer_class = RepurchaseSerializer


# 股票视图
class StockListView(generics.ListCreateAPIView):
    queryset = StockList.objects.all()
    serializer_class = StockListSerializer
    filterset_fields = ('ts_code', 'industry', 'area')


# 股东增减持视图
class HolderTradeView(generics.ListCreateAPIView):
    queryset = HolderTrade.objects.all()
    serializer_class = HolderTradeSerializer
    filterset_fields = ('ann_date', 'holder_type', 'in_de', 'change_ratio', 'avg_price', 'begin_date', 'close_date')


# 利润表视图
class IncomeListView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    filterset_fields = ('end_date', 'ts_code', 'revenue')


# 业绩快报
class ExpressListView(generics.ListCreateAPIView):
    queryset = Express.objects.all()
    serializer_class = ExpressSerializer
    filterset_fields = ('ts_code', 'end_date', 'revenue')


# 基金列表、持仓视图
class FundListView(generics.ListCreateAPIView):
    queryset = FundList.objects.all()
    serializer_class = FundListSerializer
    filterset_fields = ('found_date', 'due_date', 'list_date', 'delist_date')

class FundPortfolioListView(generics.ListCreateAPIView):
    queryset = FundPortfolio.objects.all()
    serializer_class = FundPortfolioSerializer
    filterset_fields = ('ts_code', 'end_date')


# 指数视图
class IndexListView(generics.ListCreateAPIView):
    queryset = IndexList.objects.all()
    serializer_class = IndexSerializer
    filterset_fields = ('category', 'select_opt')


# 指数日K线数据
class KdataIndex(APIView):
    '''
    从tushare获取数据
    '''
    def get(self, request, tscode, start, format=None):
        '''
        指数日K线
        '''
        kdata = pro.index_daily(ts_code=tscode, start_date=start)
        kdata = kdata.fillna(0)
        kdata = kdata.sort_values(by="trade_date" , ascending=True)
        kdata = {'tscode': tscode, 'date': kdata['trade_date'].tolist(), 'close':kdata['close'].tolist()}
        return Response(kdata)

# 国外指数数据
class KdataIndexGlobal(APIView):
    '''
    从tushare获取数据
    '''
    def get(self, request, start, end, format=None):
        '''
        国际指数
        '''
        kdata = pro.index_global(start_date=start, end_date=end)
        kdata = kdata.fillna(0)
        kdata = kdata.groupby("ts_code")
        klist = []
        for name,group in kdata:
            kd = {'tscode':name, 'date':group['trade_date'].tolist(), 'close':group['close'].tolist()}
            klist.append(kd)
        return Response(klist)