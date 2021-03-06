from django.db import models
import numpy as np
import pandas as pd
import tushare
pro = tushare.pro_api('60e379652b074a917985f88b293b702f3873c9767006d60e4d7b0875')
import time, datetime


# cbond list
class CbondList(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=9, verbose_name='转债代码')
    bond_full_name = models.CharField(max_length=50, verbose_name='转债名称')
    bond_short_name = models.CharField(max_length=30, verbose_name='转债简称')
    stk_code = models.CharField(max_length=9, verbose_name='正股代码')
    stk_short_name = models.CharField(max_length=50, verbose_name='正股简称')
    maturity = models.FloatField(verbose_name='发行期限（年）')
    par = models.FloatField(verbose_name='面值')
    issue_price = models.FloatField(verbose_name='发行价格')
    issue_size = models.FloatField(verbose_name='发行总额（亿元）')
    remain_size = models.FloatField(verbose_name='债券余额（亿元）')
    value_date = models.CharField(max_length=10, verbose_name='起息日期')
    maturity_date = models.CharField(max_length=10, verbose_name='到期日期')
    rate_type = models.CharField(max_length=5000, verbose_name='利率类型')
    coupon_rate = models.FloatField(verbose_name='票面利率（%）')
    add_rate = models.FloatField(verbose_name='补偿利率（%）')
    pay_per_year = models.FloatField(verbose_name='年付息次数')
    list_date = models.CharField(max_length=10, verbose_name='上市日期')
    delist_date = models.CharField(max_length=10, verbose_name='摘牌日')
    exchange = models.CharField(max_length=10, verbose_name='上市地点')
    conv_start_date = models.CharField(max_length=10, verbose_name='转股起始日')
    conv_end_date = models.CharField(max_length=10, verbose_name='转股截止日')
    first_conv_price = models.FloatField(verbose_name='初始转股价')
    conv_price = models.FloatField(verbose_name='最新转股价')
    rate_clause = models.CharField(max_length=5000, verbose_name='利率说明')
    put_clause = models.CharField(max_length=5000, verbose_name='赎回条款')
    maturity_put_price = models.CharField(max_length=500, verbose_name='到期赎回价格(含税)')
    call_clause = models.CharField(max_length=5000, verbose_name='回售条款')
    reset_clause = models.CharField(max_length=5000, verbose_name='特别向下修正条款')
    conv_clause = models.CharField(max_length=5000, verbose_name='转股条款')
    guarantor = models.CharField(max_length=50, verbose_name='担保人')
    guarantee_type = models.CharField(max_length=50, verbose_name='担保方式')
    issue_rating = models.CharField(max_length=50, verbose_name='发行信用等级')
    newest_rating = models.CharField(max_length=50, verbose_name='最新信用等级')
    rating_comp = models.CharField(max_length=50, verbose_name='最新评级机构')

    class Meta:
        db_table = 'cbond_list'

    def __str__(self):
        return self.ts_code


def updateCbond(date=None):
    try:
        if not date:
            date = time.strftime('%Y%m%d', time.localtime())
        rlist = pro.cb_basic(list_date=date)
    except:
        send_mail('获取失败', '{}获取可转债信息失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
        rlist = pd.DataFrame()
    # 整理
    rlist = rlist.replace(np.nan, 0)
    if not rlist.empty:
        for idx,row in rlist.iterrows():
            record = row.to_dict()
            cbond = CbondList(**record)
            cbond.save()