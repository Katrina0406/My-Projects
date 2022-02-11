from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import math
import requests
import logging
import datetime
from tqsdk import TqApi, TqAuth
import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR
import pymysql
url = '39.106.184.170'
username = 'MarketData'
password = 'Chenshi20190201.'
database = 'MarketData'


api = TqApi(auth=TqAuth("csadam", "Chenshi2019")) # 天勤登录 用户名 密码

def getLastestPrice(request, ticker):
    """
    期货最新价格实时数据接口 新浪财经
    input: ticker eg. SHFE.au2106
    return: lastestPrice 期货最新价格
    """
    exchange = ticker.split('.')[0]
    if exchange == 'CZCE':
        # 郑商所Ticker转换 CZCE CF105 -> CZCE.CF2105
         ticker = ticker.split('.')[1][0:2] + str(datetime.datetime.now().year)[2] + ticker.split('.')[1][2:5]
        #ticker = ticker.split(".")[1].upper()
    else:
        ticker = ticker.split('.')[1].upper()
    try:

        #ZC2105
        urlhead = 'http://hq.sinajs.cn/list=nf_'+ticker
        reqdata = requests.get(urlhead).content.decode('gbk')
        datalist = reqdata.split('"')[1].split(',')
        if exchange == 'CFFEX':
            lastestPrice = datalist[3] # CFFEX 中国金融期货交易所

        else:
            lastestPrice = datalist[8]  # CZCE DCE SHFE (INE)
    except:
        lastestPrice = ''
    return HttpResponse(lastestPrice)


def getSettelmentPrice(request, ticker):
    """
    期货最新价格实时数据接口 新浪财经
    input: ticker eg. SHFE.au2106
    return: lastestPrice 期货最新价格
    """
    exchange = ticker.split('.')[0].upper()
    if exchange == 'CZCE':
        # 郑商所Ticker转换 CZCE CF105 -> CZCE.CF210
        ticker = ticker.split(".")[1]
        # #CZCE.ZC2105
        # print(ticker.split('.')[1][0:2])
        # print(str(datetime.datetime.now().year)[2:4])
        # print(ticker.split('.')[1][2:5])
        # ticker = ticker.split('.')[1][0:2] + str(datetime.datetime.now().year)[2] + ticker.split('.')[1][2:5]
    else:
        ticker = ticker.split('.')[1].upper()
    try:
        urlhead = 'http://hq.sinajs.cn/list=nf_'+ticker
        reqdata = requests.get(urlhead).content.decode('gbk')
        datalist = reqdata.split('"')[1].split(',')
        if exchange == 'CFFEX':
            settelmentPrice = datalist[7] # CFFEX 中国金融期货交易所
        else:
            settelmentPrice = datalist[9] # CZCE DCE SHFE (INE)
    except:
        settelmentPrice = ''
    return HttpResponse(settelmentPrice)


def getTQLastPrice(request, ticker):
    """
    期货合约最新市场价格接口 Tianqin
    :param ticker: 期货合约ticker SHFE.au2102 CZCE.AP105 适用于期货组合 DCE.SP jm2104&jm2106
    :return: 期货合约最新市场价格
    """
    quote = api.get_quote(ticker)
    api.wait_update(time.time() + 0.3) # 阻塞函数 数据更新 等待截止时间=当前时间+等待时间(0.3)

    # 组合合约
    if '&' in ticker:
        exchange = ticker.split('.')[0]
        tk0 = ticker.split(' ')[1].split('&')[0]
        tk1 = ticker.split(' ')[1].split('&')[1]
        quote0 = api.get_quote(exchange + '.' + tk0)
        quote1 = api.get_quote(exchange + '.' + tk1)
        price = quote0.last_price - quote1.last_price
        price.__round__(2)
        return HttpResponse(price)

    else:
        price = quote.last_price
        price.__round__(2)
        return HttpResponse(price)


def getTQCloseAndSettle(request, ticker):
    """
    期货合约收盘价和结算价接口 Tianqin
    :param ticker: 期货合约ticker SHFE.au2102 CZCE.AP105 不适用于期货组合
    :return: 期货合约收盘价和结算价
    """
    quote = api.get_quote(ticker)
    api.wait_update(time.time() + 0.3)  # 阻塞函数 数据更新 等待截止时间=当前时间+等待时间(0.3)
    res = {"datetime": quote.datetime, "close": None, "settle": None}

    # 收盘价
    if math.isnan(quote.close):
        if math.isnan(quote.pre_close):
            res["close"] = None                             # 当天没数据 昨天没数据 返回 None
        else:
            res["close"] = quote.pre_close.__round__(2)     # 当天没数据 昨天有数据 返回 pre_close
    else:
        res["close"] = quote.close.__round__(2)             # 当天有数据 返回 close

    # 结算价
    if math.isnan(quote.settlement):
        if math.isnan(quote.pre_settlement):
            res["settle"] = None
        else:
            res["settle"] = quote.pre_settlement.__round__(2)
    else:
        res["settle"] = quote.settlement.__round__(2)

    return JsonResponse(res)


def getMarginRate(request, ticker, buy_or_sell, hedge_or_speculate):
    """
    :param ticker: ticker
    :param trade_date: 8位字符串 "20210324"
    :param buy_or_sell: 1 - buy, 0 - sell
    :param hedge_or_speculate: 1 - hedge, 0 speculate
    :return: res: Json格式
    """
    # b_hedging_margin_rate 买套保交易保证金率
    # s_hedging_margin_rate 卖套保交易保证金率
    # long_margin_rate 买投机交易保证金率
    # short_margin_rate 卖投机交易保证金率

    if buy_or_sell == '1':
        if hedge_or_speculate == '1':
            res_type  = "b_hedging_margin_rate"
            res_index = 8
        else: # hedge_or_speculate == 0
            res_type  = "long_margin_rate"
            res_index = 10
    else: # buy_or_sell == 0
        if hedge_or_speculate == '1':
            res_type  = "s_hedging_margin_rate"
            res_index = 9
        else: # hedge_or_speculate == 0
            res_type  = "short_margin_rate"
            res_index = 11

    db = pymysql.connect(host=url, user=username, password=password, db=database,
                         port=3306, charset="utf8")
    cursor = db.cursor()
    sql = 'SELECT * FROM future_latest_contract_settle WHERE ticker = %s order by trade_date desc limit 0,1'
    cursor.execute(sql,ticker)
    result = cursor.fetchall()

    if len(result)<=0:
        res = {"ticker":ticker,"trade_date":"",res_type:0.0}
    else:
        res = {"ticker": ticker, "trade_date": result[0][3], res_type: result[0][res_index]}

    cursor.close()
    db.close()
    return JsonResponse(res)





def closeTQ(request):
    api.close() # 账号登出 可选
    return HttpResponse('Logout!')
    # 目前可以使用以下代码来获取所有合约代码列表:




# 连接数据库
engine = create_engine("mysql+pymysql://"+username+":"+password+"@"+url+":3306/"+database+"?charset=utf8")
db = pymysql.connect(host=url, user=username, password=password, db=database, port=3306, charset="utf8")

# 获取期货套利合约动态表
def getFuturePortfolioDynamic(combineList):
    """
    获取并构建期货套利组合动态表
    :arg combineList
    :return table_dynamic_port
    """

    # Step1: 跨期跨品种期货组合ticker由函数输入给出combineList

    # Step2: 根据ticker从TQAPI获取动态表相关数据
    ticker, symbol, exchange, commodity_type, ins_class, expired, trading_time, delist_date = [[None] * len(combineList)
                                                                                               for _ in range(8)]
    for i in range(len(combineList)):
        # for i in range(10):
        currentOne = api.get_quote(combineList[i])

        ticker[i] = currentOne.instrument_id
        symbol[i] = ticker[i].split('.')[1]
        exchange[i] = currentOne.exchange_id
        commodity_type[i] = currentOne.product_id
        ins_class[i] = currentOne.ins_class
        expired[i] = 1 if currentOne.expired == True else 0
        trading_time[i] = str(currentOne.trading_time)
        delist_date[i] = time.strftime("%Y%m%d", time.localtime(currentOne.expire_datetime))

    table_dynamic_port = pd.DataFrame(
        {"ticker": ticker, "symbol": symbol, "exchange": exchange, "commodity_type": commodity_type,
         "ins_class": ins_class, "expired": expired, "trading_time": trading_time, "delist_date": delist_date})

    # Step3: 通过基本合约信息补充组合信息 list_date d_month last_ddate is_main_contract
    table_dynamic_port["list_date"] = ""
    table_dynamic_port["d_month"] = ""
    table_dynamic_port["last_ddate"] = ""
    table_dynamic_port["is_main_contract"] = ""
    table_dynamic_port["update_time"] = ""
    table_dynamic = pd.read_sql_table("future_contract_dynamic", engine)
    for i in table_dynamic_port.index:
        contract0 = table_dynamic_port["symbol"][i].split(' ')[1].split('&')[0]
        contract1 = table_dynamic_port["symbol"][i].split(' ')[1].split('&')[1]

        # list_date
        try:
            con_date0 = table_dynamic["list_date"][table_dynamic["symbol"] == contract0.upper()]
            con_date0 = con_date0[con_date0.index[0]]
            con_date1 = table_dynamic["list_date"][table_dynamic["symbol"] == contract1.upper()]
            con_date1 = con_date1[con_date1.index[0]]
            if int(con_date0) <= int(con_date1):
                table_dynamic_port.loc[i, "list_date"] = con_date0
            else:
                table_dynamic_port.loc[i, "list_date"] = con_date1
        except:
            table_dynamic_port.loc[i, "list_date"] = None

        # d_month
        try:
            con_dm0 = table_dynamic["d_month"][table_dynamic["symbol"] == contract0.upper()]
            con_dm0 = con_dm0[con_dm0.index[0]]
            con_dm1 = table_dynamic["d_month"][table_dynamic["symbol"] == contract1.upper()]
            con_dm1 = con_dm1[con_dm1.index[0]]
            if int(con_dm0) <= int(con_dm1):
                table_dynamic_port.loc[i, "d_month"] = con_dm0
            else:
                table_dynamic_port.loc[i, "d_month"] = con_dm1
        except:
            table_dynamic_port.loc[i, "d_month"] = None

        # last_ddate
        try:
            con_ldd0 = table_dynamic["last_ddate"][table_dynamic["symbol"] == contract0.upper()]
            con_ldd0 = con_ldd0[con_ldd0.index[0]]
            con_ldd1 = table_dynamic["last_ddate"][table_dynamic["symbol"] == contract1.upper()]
            con_ldd1 = con_ldd1[con_ldd1.index[0]]
            if int(con_ldd0) <= int(con_ldd1):
                table_dynamic_port.loc[i, "last_ddate"] = con_ldd0
            else:
                table_dynamic_port.loc[i, "last_ddate"] = con_ldd1
        except:
            table_dynamic_port.loc[i, "last_ddate"] = None

        # is_main_contract
        try:
            con_ismain0 = table_dynamic["is_main_contract"][table_dynamic["symbol"] == contract0.upper()]
            con_ismain0 = con_ismain0[con_ismain0.index[0]]
            con_ismain1 = table_dynamic["is_main_contract"][table_dynamic["symbol"] == contract1.upper()]
            con_ismain1 = con_ismain1[con_ismain1.index[0]]
            if con_ismain0 == "True" and con_ismain1 == "True":
                table_dynamic_port.loc[i, "is_main_contract"] = con_ismain0
            else:
                table_dynamic_port.loc[i, "is_main_contract"] = "False"
        except:
            table_dynamic_port.loc[i, "is_main_contract"] = None

        # update_time
        table_dynamic_port.loc[i, "update_time"] = str(time.strftime('%Y-%m-%d %H:%M:%S'))

    # Step4: 数据返回pandas.DataFrame table_dynamic_port
    return table_dynamic_port

# 获取期货套利合约静态表
def getFuturePortfolioStatic(new_static_table):
    """
    构建期货套利组合静态表
    :arg new_static_table
    :return table_static_port
    """
    table_static = pd.read_sql_table("future_contract_static", engine)

    table_static_port = new_static_table
    table_static_port["exchange_name"] = ""
    # table_static_port["strategy"] = ""
    table_static_port["commodity_type_name"] = ""
    table_static_port["contract_size_unit"] = ""
    table_static_port["contract_size"] = ""
    table_static_port["contract_currency"] = "CNY"  # contract_currency
    table_static_port["contract_currency_unit"] = "人民币元"  # contract_currency_unit
    table_static_port["unit"] = ""
    table_static_port["quote_unit_desc"] = ""
    table_static_port["delivery_method"] = ""
    table_static_port["update_time"] = ""

    for i in table_static_port.index:
        # 交易所名称
        if table_static_port["exchange"][i] == "DCE":
            table_static_port["exchange_name"][i] = "大连商品交易所"
        elif table_static_port["exchange"][i] == "CZCE":
            table_static_port["exchange_name"][i] = "郑州商品交易所"

        # 套利策略
        # strategy = table_static_port["commodity_type"][i].split(' ')[0]
        # if strategy == "SP" or strategy == "SPD":
        #     table_static_port["strategy"][i] = "跨期套利"
        # elif strategy == "SPC" or strategy == "IPS":
        #     table_static_port["strategy"][i] = "跨品种套利"

        # 商品种类
        try:
            comb_type = table_static_port["commodity_type"][i].split(' ')[1].split('&')
            comb_name0 = table_static["commodity_type_name"][table_static["ts_commodity_type"] == comb_type[0].upper()]
            comb_name0 = comb_name0[comb_name0.index[0]]
            comb_name1 = table_static["commodity_type_name"][table_static["ts_commodity_type"] == comb_type[1].upper()]
            comb_name1 = comb_name1[comb_name1.index[0]]
            table_static_port["commodity_type_name"][i] = comb_name0 + "和" + comb_name1
        except:
            table_static_port["commodity_type_name"][i] = None

        # contract_size_unit
        try:
            comb_size0 = table_static["contract_size_unit"][table_static["ts_commodity_type"] == comb_type[0].upper()]
            comb_size0 = comb_size0[comb_size0.index[0]]
            comb_size1 = table_static["contract_size_unit"][table_static["ts_commodity_type"] == comb_type[1].upper()]
            comb_size1 = comb_size1[comb_size1.index[0]]
            if comb_size0 == comb_size1:
                table_static_port["contract_size_unit"][i] = comb_size0
            else:
                table_static_port["contract_size_unit"][i] = None
        except:
            table_static_port["contract_size_unit"][i] = None

        # contract_size
        try:
            con_size0 = table_static["contract_size"][table_static["ts_commodity_type"] == comb_type[0].upper()]
            con_size0 = con_size0[con_size0.index[0]]
            con_size1 = table_static["contract_size"][table_static["ts_commodity_type"] == comb_type[1].upper()]
            con_size1 = con_size1[con_size1.index[0]]
            if con_size0 == con_size1:
                table_static_port["contract_size"][i] = con_size0
            else:
                table_static_port["contract_size"][i] = None
        except:
            table_static_port["contract_size"][i] = None

        # unit
        try:
            con_unit0 = table_static["unit"][table_static["ts_commodity_type"] == comb_type[0].upper()]
            con_unit0 = con_unit0[con_unit0.index[0]]
            con_unit1 = table_static["unit"][table_static["ts_commodity_type"] == comb_type[1].upper()]
            con_unit1 = con_unit1[con_unit1.index[0]]
            if con_unit0 == con_unit1:
                table_static_port["unit"][i] = con_unit0
            else:
                table_static_port["unit"][i] = None
        except:
            table_static_port["unit"][i] = None

        # quote_unit_desc
        try:
            con_unitd0 = table_static["quote_unit_desc"][table_static["ts_commodity_type"] == comb_type[0].upper()]
            con_unitd0 = con_unitd0[con_unitd0.index[0]]
            con_unitd1 = table_static["quote_unit_desc"][table_static["ts_commodity_type"] == comb_type[1].upper()]
            con_unitd1 = con_unitd1[con_unitd1.index[0]]
            if con_unitd0 == con_unitd1:
                table_static_port["quote_unit_desc"][i] = con_unitd0
            else:
                table_static_port["quote_unit_desc"][i] = None
        except:
            table_static_port["quote_unit_desc"][i] = None

        # delivery_method
        try:
            con_dm0 = table_static["delivery_method"][table_static["ts_commodity_type"] == comb_type[0].upper()]
            con_dm0 = con_dm0[con_dm0.index[0]]
            con_dm1 = table_static["delivery_method"][table_static["ts_commodity_type"] == comb_type[1].upper()]
            con_dm1 = con_dm1[con_dm1.index[0]]
            if con_dm0 == con_dm1:
                table_static_port["delivery_method"][i] = con_dm0
            else:
                table_static_port["delivery_method"][i] = None
        except:
            table_static_port["delivery_method"][i] = None

        # update_time
        table_static_port["update_time"][i] = str(time.strftime('%Y-%m-%d:%H:%M:%S'))
    return table_static_port

# 更新动态表期货组合数据
def getAllFuturePortfolio(request):
    """
    更新动态表期货组合数据 调用 getFuturePortfolioDynamic(combineList)
    更新静态表期货组合数据 调用 getFuturePortfolioStatic(new_static_table)
    """

    """
    Scenario 1: 新的期货组合上市
    """
    # 1.1 数据库中的ticker
    table_dynamic = pd.read_sql_table("future_contract_dynamic", engine)
    table_dynamic_ticker = list(table_dynamic["ticker"][(table_dynamic.ins_class == "COMBINE")])
    # 1.2 市场上所有的ticker
    combine_ticker_all = api.query_quotes(ins_class='COMBINE')

    new_ticker = []

    for i in combine_ticker_all:
        if i not in table_dynamic_ticker:
            new_ticker.append(i)

    if new_ticker == []:
        msg = "<br>动态表无新合约出现！</br>"
    else:
        table_dynamic_port = getFuturePortfolioDynamic(new_ticker)
        DTYPES_dynamic = {'ticker': VARCHAR(255), 'symbol': VARCHAR(255), 'exchange': VARCHAR(255),
                          'commodity_type': VARCHAR(255), 'ins_class': VARCHAR(255), 'expired': VARCHAR(255),
                          'trading_time': VARCHAR(255), 'delist_date': VARCHAR(255), 'list_date': VARCHAR(255),
                          'd_month': VARCHAR(255), 'last_ddate': VARCHAR(255), 'update_time': VARCHAR(255),
                          'is_main_contract': VARCHAR(255)}
        table_dynamic_port.to_sql("future_contract_dynamic", engine, index=False, if_exists='append', dtype=DTYPES_dynamic)
        msg = "<br>动态表新合约"+ str(len(new_ticker)) + "条更新完成！</br>"

    """
    Scenario 2: 之前未到期 当前到期的期货组合合约 修改expired字段 0->1 
    """
    # 2.1 从动态表数据库获取未到期合约（历史数据）
    historical_not_expired = list(table_dynamic["ticker"][(table_dynamic.ins_class == "COMBINE") & (table_dynamic.expired == "0")])
    # 2.2 根据ticker从TQAPI获取动态表到期合约（当前数据）
    current_expired = api.query_quotes(ins_class='COMBINE', expired=True)

    expired_list = []
    for i in historical_not_expired:
        if i in current_expired:
            expired_list.append(i)

    if expired_list == []:
        msg += "<br>动态表无合约到期！</br>"
    else:
        for i in expired_list:
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            # SQL语句更新数据
            sql = """ UPDATE future_contract_dynamic SET expired = "1" WHERE ticker = "%s" """ % i
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        msg += "<br>动态表到期合约数据"+ str(len(expired_list)) + "条更新完成！</br>"

    """
    更新静态表期货组合数据 调用 getFuturePortfolioStatic(new_static_table)
    """
    # 数据库静态表中的合约列表
    table_static = pd.read_sql_table("future_contract_static", engine)
    static_list = list(table_static["commodity_type"])
    # 市场上的全部合约列表
    table_static_port = pd.read_sql_table("future_contract_dynamic", engine)
    table_static_port = table_static_port[["exchange", "commodity_type"]].drop_duplicates()

    index_new = []
    for i in table_static_port.index:
        if table_static_port.loc[i, "commodity_type"] not in static_list and '&' in table_static_port.loc[i, "commodity_type"]:
            index_new.append(i)

    if index_new == []:
        msg += "<br>静态表无期货组合新品种！</br>"
    else:
        new_static_table = table_static_port.loc[index_new, :]
        table_static_port = getFuturePortfolioStatic(new_static_table)
        DTYPES_static = {'ts_code': VARCHAR(255), 'exchange': VARCHAR(255), 'exchange_name': VARCHAR(255),
                         'commodity_type': VARCHAR(255), 'commodity_type_name': VARCHAR(255),
                         'ts_commodity_type': VARCHAR(255),
                         'multiplier': VARCHAR(255), 'contract_size_unit': VARCHAR(255), 'contract_size': VARCHAR(255),
                         'contract_currency': VARCHAR(255), 'contract_currency_unit': VARCHAR(255),
                         'unit': VARCHAR(255),
                         'quote_unit_desc': VARCHAR(255), 'delivery_method': VARCHAR(255), 'update_time': VARCHAR(255)}
        table_static_port.to_sql("future_contract_static", engine, index=False, if_exists='append', dtype=DTYPES_static)
        msg += "<br>静态表期货组合新品种" + str(new_static_table.shape[0]) + "条更新完成！</br>"

    msg += "<br>动静态表更新完成！</br>"
    return HttpResponse(msg)
