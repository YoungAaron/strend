from django.db import models
from django.core.mail import send_mail
import numpy as np
import pandas as pd
import tushare
pro = tushare.pro_api('60e379652b074a917985f88b293b702f3873c9767006d60e4d7b0875')
import time, datetime


# 返回开始和结束之间的所有日期
def sqday(begin_date, end_date):
    begin_date = datetime.datetime.strptime(begin_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    date_sq_list = []
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        date_sq_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_sq_list

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
    

# 行业列表
class IndustryList(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'industry_list'


# 指数列表
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
    select_opt = models.CharField(max_length=30, default=0, verbose_name='选择参数')

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

# 股票回购
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
    rlist = rlist.replace(np.nan, 0)
    rlist = rlist[rlist['proc'] == '股东大会通过']
    # 入库
    if not rlist.empty:
        for idx,row in rlist.iterrows():
            record = row.to_dict()
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


# 股东增减持
class HolderTrade(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=15, verbose_name='TS代码')
    ann_date = models.CharField(max_length=8, verbose_name='公告日期')
    holder_name = models.CharField(max_length=60, verbose_name='股东名称')
    holder_type = models.CharField(max_length=3, verbose_name='股东类型G高管P个人C公司')
    in_de = models.CharField(max_length=3, verbose_name='类型')
    change_vol = models.FloatField(verbose_name='变动数量')
    change_ratio = models.FloatField(verbose_name='占流通比例（%）')
    after_share = models.FloatField(verbose_name='变动后持股')
    after_ratio = models.FloatField(verbose_name='变动后占流通比例（%）')
    avg_price = models.FloatField(verbose_name='平均价格')
    total_share = models.FloatField(verbose_name='持股总数')
    begin_date = models.CharField(max_length=15, verbose_name='开始日期')
    close_date = models.CharField(max_length=15, verbose_name='结束日期')

    class Meta:
        db_table = 'holder_trade'

def update_holdertrade(date=None):
    try:
        if not date:
            date = time.strftime('%Y%m%d', time.localtime())
        rlist = pro.stk_holdertrade(ann_date=date)
    except:
        send_mail('获取失败', '{}获取股东增减持信息失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
        rlist = pd.DataFrame()
    # 整理
    rlist = rlist.replace(np.nan, 0)
    if not rlist.empty:
        for idx,row in rlist.iterrows():
            record = row.to_dict()
            holdertrade = HolderTrade(**record)
            holdertrade.save()


# 股东人数
class HolderNumber(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=15, verbose_name='TS代码')
    ann_date = models.CharField(max_length=8, verbose_name='公告日期')
    end_date = models.CharField(max_length=8, verbose_name='截止日期')
    holder_num = models.FloatField(verbose_name='股东户数')

    class Meta:
        db_table = 'holder_number'

def update_holdernumber(date=None):
    try:
        if not date:
            date = time.strftime('%Y%m%d', time.localtime())
        rlist = pro.stk_holdernumber(start_date=date, end_date=date)
    except:
        send_mail('获取失败', '{}获取股东人数信息失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
        rlist = pd.DataFrame()
    # 整理
    rlist = rlist.replace(np.nan, 0)
    if not rlist.empty:
        for idx,row in rlist.iterrows():
            record = row.to_dict()
            holder = HolderNumber(**record)
            holder.save()


# 股票账户开户数据
class TraderAccount(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=15, verbose_name='统计周期')
    weekly_new = models.FloatField(verbose_name='本周新增（万）')
    total = models.FloatField(verbose_name='期末总账户数（万）')
    weekly_hold = models.FloatField(verbose_name='本周持仓账户数（万）')
    weekly_trade = models.FloatField(verbose_name='本周参与交易账户数（万）')

    class Meta:
        db_table = 'trader_account'

def update_traderaccount(date=None):
    try:
        if not date:
            date = time.strftime('%Y%m%d', time.localtime())
        rlist = pro.stk_account(date=date)
    except:
        send_mail('获取失败', '{}获取利润表信息失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
        rlist = pd.DataFrame()
    # 整理
    rlist = rlist.replace(np.nan, 0)
    if not rlist.empty:
        for idx,row in rlist.iterrows():
            record = row.to_dict()
            account = TraderAccount(**record)
            account.save()

# 利润表
class Income(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=15, verbose_name='TS代码')
    ann_date = models.CharField(max_length=15, verbose_name='公告日期')
    f_ann_date = models.CharField(max_length=15, verbose_name='实际公告日期')
    end_date = models.CharField(max_length=15, verbose_name='报告期')
    report_type = models.CharField(max_length=15, verbose_name='报告类型')
    comp_type = models.CharField(max_length=1, verbose_name='公司类型(1一般工商业2银行3保险4证券)')
    basic_eps = models.FloatField(verbose_name='基本每股收益') 
    diluted_eps = models.FloatField(verbose_name='稀释每股收益')  
    total_revenue = models.FloatField(verbose_name='营业总收入') 
    revenue = models.FloatField(verbose_name='营业收入')  
    int_income = models.FloatField(verbose_name='利息收入') 
    prem_earned = models.FloatField(verbose_name='已赚保费') 
    comm_income = models.FloatField(verbose_name='手续费及佣金收入')
    n_commis_income = models.FloatField(verbose_name='手续费及佣金净收入')
    n_oth_income = models.FloatField(verbose_name='其他经营净收益')
    n_oth_b_income = models.FloatField(verbose_name='其他业务净收益')
    prem_income = models.FloatField(verbose_name='保险业务收入')  
    out_prem = models.FloatField(verbose_name='分出保费')
    une_prem_reser = models.FloatField(verbose_name='提取未到期责任准备金') 
    reins_income = models.FloatField(verbose_name='分保费收入')
    n_sec_tb_income = models.FloatField(verbose_name='代理买卖证券业务净收入')
    n_sec_uw_income = models.FloatField(verbose_name='证券承销业务净收入') 
    n_asset_mg_income = models.FloatField(verbose_name='受托客户资产管理业务净收入') 
    oth_b_income = models.FloatField(verbose_name='其他业务收入')
    fv_value_chg_gain = models.FloatField(verbose_name='公允价值变动净收益')
    invest_income = models.FloatField(verbose_name='投资净收益')
    ass_invest_income = models.FloatField(verbose_name='对联营企业和合营企业的投资收益')
    forex_gain = models.FloatField(verbose_name='汇兑净收益')
    total_cogs = models.FloatField(verbose_name='营业总成本')
    oper_cost = models.FloatField(verbose_name='营业成本')
    int_exp = models.FloatField(verbose_name='利息支出')
    comm_exp = models.FloatField(verbose_name='手续费及佣金支出')
    biz_tax_surchg = models.FloatField(verbose_name='营业税金及附加')
    sell_exp = models.FloatField(verbose_name='销售费用')
    admin_exp = models.FloatField(verbose_name='管理费用')
    fin_exp = models.FloatField(verbose_name='财务费用')
    assets_impair_loss = models.FloatField(verbose_name='资产减值损失')
    prem_refund = models.FloatField(verbose_name='退保金')
    compens_payout = models.FloatField(verbose_name='赔付总支出')
    reser_insur_liab = models.FloatField(verbose_name='提取保险责任准备金')
    div_payt = models.FloatField(verbose_name='保户红利支出')
    reins_exp = models.FloatField(verbose_name='分保费用') 
    oper_exp = models.FloatField(verbose_name='营业支出')  
    compens_payout_refu = models.FloatField(verbose_name='摊回赔付支出')
    insur_reser_refu = models.FloatField(verbose_name='摊回保险责任准备金')
    reins_cost_refund = models.FloatField(verbose_name='摊回分保费用')
    other_bus_cost = models.FloatField(verbose_name='其他业务成本') 
    operate_profit = models.FloatField(verbose_name='营业利润') 
    non_oper_income = models.FloatField(verbose_name='营业外收入')
    non_oper_exp = models.FloatField(verbose_name='营业外支出')
    nca_disploss = models.FloatField(verbose_name='非流动资产处置净损失')
    total_profit = models.FloatField(verbose_name='利润总额') 
    income_tax = models.FloatField(verbose_name='所得税费用')
    n_income = models.FloatField(verbose_name='净利润(含少数股东损益)')  
    n_income_attr_p = models.FloatField(verbose_name='净利润(不含少数股东损益)')
    minority_gain = models.FloatField(verbose_name='少数股东损益')
    oth_compr_income = models.FloatField(verbose_name='其他综合收益')  
    t_compr_income = models.FloatField(verbose_name='综合收益总额') 
    compr_inc_attr_p = models.FloatField(verbose_name='归属于母公司(或股东)的综合收益总额') 
    compr_inc_attr_m_s = models.FloatField(verbose_name='归属于少数股东的综合收益总额')  
    ebit = models.FloatField(verbose_name='息税前利润') 
    ebitda = models.FloatField(verbose_name='息税折旧摊销前利润')   
    insurance_exp = models.FloatField(verbose_name='保险业务支出') 
    undist_profit = models.FloatField(verbose_name='年初未分配利润') 
    distable_profit = models.FloatField(verbose_name='可分配利润')
    update_flag = models.CharField(max_length=15, verbose_name='公告日期')

    class Meta:
        db_table = 'income'

def update_income(date=None):
    if not date:
        date = time.strftime('%Y%m%d', time.localtime())
    for tc in StockList.objects.all():
        try:
            rlist = pro.income(ann_date=date, ts_code=tc.ts_code)
        except:
            send_mail('获取失败', '{}获取利润表信息失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
            rlist = pd.DataFrame()
        # 整理
        rlist = rlist.replace(np.nan, 0)
        if not rlist.empty:
            for idx,row in rlist.iterrows():
                record = row.to_dict()
                income = Income(**record)
                income.save()


# 业绩快报
class Express(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=15, verbose_name='TS股票代码')
    ann_date = models.CharField(max_length=8, verbose_name='公告日期')
    end_date = models.CharField(max_length=8, verbose_name='报告期')
    revenue = models.FloatField(verbose_name='营业收入(元)')
    operate_profit = models.FloatField(verbose_name='营业利润(元)')
    total_profit = models.FloatField(verbose_name='利润总额(元)')	
    n_income = models.FloatField(verbose_name='净利润(元)')
    total_assets = models.FloatField(verbose_name='总资产(元)')
    total_hldr_eqy_exc_min_int = models.FloatField(verbose_name='股东权益合计(不含少数股东权益)(元)')
    diluted_eps = models.FloatField(verbose_name='每股收益(摊薄)(元)')
    diluted_roe = models.FloatField(verbose_name='净资产收益率(摊薄)(%)')	
    yoy_net_profit = models.FloatField(verbose_name='去年同期修正后净利润')
    bps = models.FloatField(verbose_name='每股净资产')
    perf_summary = models.CharField(max_length=600, verbose_name='业绩简要说明')	
    
    class Meta:
        db_table = 'express'

def update_express(date=None):
    try:
        if not date:
            date = time.strftime('%Y%m%d', time.localtime())
        rlist = pro.express(ann_date=date)
    except:
        send_mail('获取失败', '{}获取业绩快报信息失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
        rlist = pd.DataFrame()
    # 整理
    rlist = rlist.replace(np.nan, 0)
    if not rlist.empty:
        for idx,row in rlist.iterrows():
            record = row.to_dict()
            express = Express(**record)
            express.save()


# 融资融券交易汇总
class Margin(models.Model):
    id = models.AutoField(primary_key=True)
    trade_date = models.CharField(max_length=8, verbose_name='交易日期')
    exchange_id = models.CharField(max_length=8, verbose_name='交易所代码（SSE上交所SZSE深交所）')
    rzye = models.FloatField(verbose_name='融资余额(元)')	
    rzmre = models.FloatField(verbose_name='融资买入额(元)')
    rzche = models.FloatField(verbose_name='融资偿还额(元)')	
    rqye = models.FloatField(verbose_name='融券余额(元)')	
    rqmcl = models.FloatField(verbose_name='融券卖出量(股,份,手)')	
    rzrqye = models.FloatField(verbose_name='融资融券余额(元)')	
    rqyl = models.FloatField(verbose_name='融券余量(股,份,手)')
    
    class Meta:
        db_table = 'margin'

def update_margin(date=None):
    try:
        if not date:
            date = time.strftime('%Y%m%d', time.localtime())
        rlist = pro.margin(trade_date=date)
    except:
        send_mail('获取失败', '{}获取融资融券交易汇总息失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
        rlist = pd.DataFrame()
    # 整理
    rlist = rlist.replace(np.nan, 0)
    if not rlist.empty:
        for idx,row in rlist.iterrows():
            record = row.to_dict()
            margin = Margin(**record)
            margin.save()

# 股权质押统计数据
class PledgeStat(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=9, verbose_name='TS代码')
    end_date = models.CharField(max_length=8, verbose_name='截至日期')	
    pledge_count = models.FloatField(verbose_name='质押次数')
    unrest_pledge = models.FloatField(verbose_name='无限售股质押数量（万）')
    rest_pledge = models.FloatField(verbose_name='限售股份质押数量（万）')	
    total_share = models.FloatField(verbose_name='总股本')	
    pledge_ratio = models.FloatField(verbose_name='质押比例')	
    
    class Meta:
        db_table = 'pledge_stat'


# 限售股解禁
class ShareFloat(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=8, verbose_name='TS代码')
    ann_date = models.CharField(max_length=8, verbose_name='公告日期')
    float_date = models.CharField(max_length=8, verbose_name='解禁日期')	
    float_share = models.FloatField(verbose_name='流通股份')	
    float_ratio = models.FloatField(verbose_name='流通股份占总股本比率')
    holder_name = models.CharField(max_length=50, verbose_name='股东名称')
    share_type = models.CharField(max_length=50, verbose_name='股份类型')	
    
    class Meta:
        db_table = 'share_float'

def update_share_float(date=None):
    try:
        if not date:
            date = time.strftime('%Y%m%d', time.localtime())
        rlist = pro.share_float(ann_date=date)
    except:
        send_mail('获取失败', '{}获取融资融券交易汇总息失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
        rlist = pd.DataFrame()
    # 整理
    rlist = rlist.replace(np.nan, 0)
    if not rlist.empty:
        for idx,row in rlist.iterrows():
            record = row.to_dict()
            share = ShareFloat(**record)
            share.save()


# 公募基金列表+持仓数据 > 基金调仓换股分析
class FundList(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=15, verbose_name='基金代码')	
    name = models.CharField(max_length=100, verbose_name='简称')
    management = models.CharField(max_length=500, verbose_name='管理人')
    custodian = models.CharField(max_length=500, verbose_name='托管人')
    fund_type = models.CharField(max_length=100, verbose_name='投资类型')
    found_date = models.CharField(max_length=8, verbose_name='成立日期')
    due_date = models.CharField(max_length=8, verbose_name='到期日期')
    list_date = models.CharField(max_length=8, verbose_name='上市时间')
    issue_date = models.CharField(max_length=8, verbose_name='发行日期')
    delist_date = models.CharField(max_length=8, verbose_name='退市日期')
    issue_amount = models.FloatField(verbose_name='发行份额(亿)')
    m_fee = models.FloatField(verbose_name='管理费')	
    c_fee = models.FloatField(verbose_name='托管费')
    duration_year = models.FloatField(verbose_name='存续期')
    p_value = models.FloatField(verbose_name='面值')	
    min_amount = models.FloatField(verbose_name='起点金额(万元)')	
    exp_return = models.FloatField(verbose_name='预期收益率')	
    benchmark = models.CharField(max_length=300, verbose_name='业绩比较基准')
    status = models.CharField(max_length=3, verbose_name='存续状态D摘牌 I发行 L已上市')
    invest_type = models.CharField(max_length=300, verbose_name='投资风格')
    ftype = models.CharField(max_length=40, verbose_name='基金类型')
    trustee = models.CharField(max_length=50, verbose_name='受托人')
    purc_startdate = models.CharField(max_length=8, verbose_name='日常申购起始日')
    redm_startdate = models.CharField(max_length=8, verbose_name='日常赎回起始日')
    market = models.CharField(max_length=3, verbose_name='E场内O场外')
    
    class Meta:
        db_table = 'fund_list'

def update_fund_list():
    try:
        rlist = pro.fund_basic()
    except:
        send_mail('获取失败', '{}获取公募基金列表失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
        rlist = pd.DataFrame()
    # 整理
    rlist = rlist.replace(np.nan, 0)
    date = time.strftime('%Y%m%d', time.localtime())
    rlist = rlist[rlist['list_date']==date]
    if not rlist.empty:
        for idx,row in rlist.iterrows():
            record = row.to_dict()
            record['ftype'] = record['type']
            record.pop('type')
            fund_list = FundList(**record)
            fund_list.save()


class FundPortfolio(models.Model):
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(max_length=15, verbose_name='TS基金代码')
    ann_date = models.CharField(max_length=10, verbose_name='公告日期')	
    end_date = models.CharField(max_length=10, verbose_name='截止日期')	
    symbol = models.CharField(max_length=15, verbose_name='股票代码')
    mkv = models.FloatField(verbose_name='持有股票市值(元)')	
    amount = models.FloatField(verbose_name='持有股票数量（股）')
    stk_mkv_ratio = models.FloatField(verbose_name='占股票市值比')
    stk_float_ratio = models.FloatField(verbose_name='占流通股本比例')
    
    class Meta:
        db_table = 'fund_portfolio'

def update_fund_portfolio(date=None):
    try:
        if not date:
            date = time.strftime('%Y%m%d', time.localtime())
        rlist = pro.fund_portfolio(ann_date=date)
    except:
        send_mail('获取失败', '{}获取融资融券交易汇总息失败'.format(date), '623522656@qq.com', ['623522656@qq.com'], fail_silently=False)
        rlist = pd.DataFrame()
    # 整理
    rlist = rlist.replace(np.nan, 0)
    if not rlist.empty:
        for idx,row in rlist.iterrows():
            record = row.to_dict()
            fund = FundPortfolio(**record)
            fund.save()