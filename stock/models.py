from django.db import models
from django.core.mail import send_mail
import numpy as np
import pandas as pd
import tushare
pro = tushare.pro_api('60e379652b074a917985f88b293b702f3873c9767006d60e4d7b0875')
import time, datetime


# 股票列表
class StockList(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=9, verbose_name='TS代码')
    symbol = models.CharField(max_length=9, verbose_name='股票代码')
    name = models.CharField(max_length=50, verbose_name='股票名称')
    area = models.CharField(max_length=30, verbose_name='所在地域')
    industry = models.CharField(max_length=30, verbose_name='所属行业')
    fullname = models.CharField(max_length=50, verbose_name='股票全称')
    enname = models.CharField(max_length=300, verbose_name='英文全称')
    market = models.CharField(max_length=30, verbose_name='市场类型')
    exchange = models.CharField(max_length=10, verbose_name='交易所代码')
    curr_type = models.CharField(max_length=10, verbose_name='交易货币')
    list_status = models.CharField(max_length=10, verbose_name='上市状态')
    list_date = models.CharField(max_length=8, verbose_name='上市日期')
    delist_date = models.CharField(max_length=8, verbose_name='退市日期')
    is_hs = models.CharField(max_length=10, verbose_name='是否沪深港通标的')

    class Meta:
        db_table = 'stock_list'

    def __str__(self):
        return self.ts_code

def updateStock():

    from django.core.mail import send_mail
    # 获取列表
    date = time.strftime('%Y%m%d', time.localtime())
    try:
        stock_list = pro.stock_basic()
    except:
        stock_list = pd.DataFrame()
        send_mail('更新失败', '{}股票列表更新失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
    # 更新列表
    if not stock_list.empty:
        old_stock = set([stock.ts_code for stock in StockList.objects.all()])
        new_stock = set(stock_list['ts_code'])
        diff = new_stock - old_stock
        for code in diff:
            stock = stock_list[stock_list['ts_code']==code]
            stock = stock.to_dict(orient='records')[0]
            stock = StockList(**stock)
            stock.save()
    

class IndustryList(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'industry_list'


class IndexList(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=9, verbose_name='TS代码')
    name = models.CharField(max_length=30, verbose_name='简称')
    fullname = models.CharField(max_length=50, verbose_name='指数全称')
    market = models.CharField(max_length=10, verbose_name='市场')
    publisher = models.CharField(max_length=10, verbose_name='发布方')
    index_type = models.CharField(max_length=100, verbose_name='指数风格')
    category = models.CharField(max_length=50, verbose_name='指数类别')
    base_date = models.CharField(max_length=8, null=True, verbose_name='基期')
    base_point = models.FloatField(verbose_name='基点')
    list_date = models.CharField(max_length=8, null=True, verbose_name='发布日期')
    weight_rule = models.CharField(max_length=50, verbose_name='加权方式')
    desc = models.CharField(max_length=500, verbose_name='描述')
    exp_date = models.CharField(max_length=8, verbose_name='终止日期')
    fun_one = models.CharField(max_length=1, default=0, verbose_name='市场对比')
    fun_two = models.CharField(max_length=1, default=0, verbose_name='行业对比')
    fun_thd = models.CharField(max_length=1, default=0, verbose_name='市值对比')

    class Meta:
        db_table = 'index_list'

def updateIndex():
    shindex_list = pro.index_basic(market='SSE') # 获取列表
    szindex_list = pro.index_basic(market='SZSE')
    index_list = pd.concat([shindex_list,szindex_list], axis=0)
    if not index_list.empty:
        for code in index_list['ts_code']:
            index = index_list[index_list['ts_code']==code]
            index = index.to_dict(orient='records')[0]
            index = IndexList(**index)
            index.save()


class Repurchase(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=9, verbose_name='TS代码')
    ann_date = models.CharField(max_length=8, verbose_name='公告日期')
    end_date = models.CharField(max_length=8, verbose_name='截止日期')
    proc = models.CharField(max_length=50, verbose_name='进度')
    exp_date = models.CharField(max_length=8, verbose_name='过期日期')
    vol = models.FloatField(verbose_name='回购数量')
    amount = models.FloatField(verbose_name='回购金额')
    high_limit = models.FloatField(verbose_name='回购最高价')
    low_limit = models.FloatField(verbose_name='回购最低价')

    class Meta:
        db_table = 'repurchase'

def updateRepurchase(date=None):
    # 获取
    try:
        if not date:
            date = time.strftime('%Y%m%d', time.localtime())
        rlist = pro.repurchase(ann_date=date)
    except:
        send_mail('获取失败', '{}获取回购信息失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
        rlist = pd.DataFrame()
    # 整理
    rlist['end_date'] = rlist['end_date'].replace(np.nan, '-')
    rlist['exp_date'] = rlist['exp_date'].replace(np.nan, '-')
    rlist = rlist.replace(np.nan, 0)
    rlist = rlist[rlist['proc'] == '股东大会通过']
    # 入库
    if not rlist.empty:
        for code in rlist['ts_code']:
            record = rlist[rlist['ts_code']==code]
            record = record.to_dict(orient='records')[0]
            record = Repurchase(**record)
            record.save()
    # 自动化发送邮箱
    #title = '{}回购信息'.format(date)
    #if not rlist.empty:
    #    content = ['{}在{}股东大会通过回购事项，回购数量{}，金额{}'.format(r['ts_code'], r['ann_date'], r['vol'], r['amount']) 
    #               for r in rlist.iterrows()]
    #    content = '\n'.join(content)
    #else:
    #    content = '今日无回购事项'
    #send_to = ['623522656@qq.com']
    #send_mail(title, content, '623522656@qq.com', send_to, fail_silently=False)
