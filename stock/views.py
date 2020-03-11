from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from stock.models import *
from stock.serializers import *

import tushare
pro = tushare.pro_api('60e379652b074a917985f88b293b702f3873c9767006d60e4d7b0875')
import time, datetime


class RepurchaseListView(generics.ListCreateAPIView):
    queryset = Repurchase.objects.all()
    serializer_class = RepurchaseSerializer
    filterset_fields = ('ann_date', 'amount')


class RepurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repurchase.objects.all()
    serializer_class = RepurchaseSerializer


class IndexListView(generics.ListCreateAPIView):
    queryset = IndexList.objects.all()
    serializer_class = IndexSerializer
    filterset_fields = ('fun_one', 'fun_two', 'fun_thd')


class KdataIndex(APIView):
    '''
    从tushare获取数据
    '''
    def get(self, request, tscode, start, format=None):
        '''
        指数日K线
        '''
        kdata = pro.index_daily(ts_code=tscode, start_date=start)
        kdata = kdata.sort_values(by="trade_date" , ascending=True)
        kdata = {'tscode': tscode, 'date': kdata['trade_date'].tolist(), 'close':kdata['close'].tolist()}
        return Response(kdata)