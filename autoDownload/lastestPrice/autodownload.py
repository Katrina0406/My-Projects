from urllib.request import urlopen
import datetime
import ast, csv
import pandas as pd

# 获取今日日期（年月日）
today = datetime.date.today()
year = str(today.year)
month = str(today.month)
monthsub = str(today.month-1) # 用于大连商品交易所特殊的月份（比当前月份少一个月）
# 将少于10的日期前加上0
if today.month < 10:
    month0 = '0'+month
else:
    month0 = month
day = today.day
if day < 10:
    day0 = '0'+str(day)
else:
    day0 = str(day)

## 读取dat文件并转化成dictionary
def readDat(data):
    dict_data = {}

    try:
        # 将dat文件先转化成str，去掉多余的信息，保留完整的dictionary
        strLine = ''.join(data)
        start = strLine.find('[')
        end = strLine.find(']')
        dict_data = strLine[start:end+1]
    except:
        print("Record: ", data)
        raise Exception("Failed while unpacking.")
    # 将dict格式的str文件解析成dictionary
    dict_data = ast.literal_eval(dict_data)
     
    return dict_data

## 上海能源交易所dat文件解析至csv文件
def ine_csvFile(data):
    # 将dat文件转化成dictionary
    dict_data = readDat(data)

    # 按照dat里的数据标签将dictionary转化成csv文件
    csv_columns = ['INSTRUMENTID', 'TRADEFEEUNIT', 'TRADEFEERATIO', 'HEDGSHORTMARGINRATIO', 'SETTLEMENTPRICE', 'COMMODITYDELIVFEEUNIT', 'SPECLONGMARGINRATIO', 'SPECSHORTMARGINRATIO', 'HEDGLONGMARGINRATIO', 'PRODUCTID', 'PRODUCTNAME']
    csv_file = "INE_Margin.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for d in dict_data:
                writer.writerow(d)
    except IOError:
        print("I/O error")

    # 处理csv文件，将列表统一成网页手动下载时的格式
    csv_data = pd.read_csv(csv_file, low_memory = False)
    csv_df = pd.DataFrame(csv_data)
    # 将列表的英文换成对应中文
    csv_df.columns = ['交割月份', '交易手续费额(元/手)', '交易手续费率(%)', '卖套保交易保证金率', '结算价', '交割手续费', '买投机交易保证金率', '卖投机交易保证金率', '买套保交易保证金率', '商品id', '商品名称']
    # 删掉手动下载格式中不存在的列
    csv_df.drop(csv_df.columns[[9]], axis=1, inplace=True)
    # 重新排列列表的顺序
    csv_df = csv_df[['商品名称', '交割月份', '结算价', '交易手续费率(%)', '交易手续费额(元/手)', '交割手续费', '买投机交易保证金率', '买套保交易保证金率', '卖投机交易保证金率', '卖套保交易保证金率']]
    csv_df = csv_df.set_index('商品名称')
    csv_df.to_csv(csv_file)

## 上海期货交易所dat文件解析至csv文件
def shfe_csvFile(data):
    # 将dat文件转化成dictionary
    dict_data = readDat(data)

    # 按照dat里的数据标签将dictionary转化成csv文件
    csv_columns = ['COMMODITYDELIVERYFEERATION', 'COMMODITYDELIVERYFEEUNIT', 'DISCOUNTRATE', 'INSTRUMENTID', 'LONGMARGINRATIO', 'SETTLEMENTPRICE', 'SHORTMARGINRATIO', 'SPEC_LONGMARGINRATIO', 'SPEC_SHORTMARGINRATIO', 'TRADEFEERATION', 'TRADEFEEUNIT', 'TRADINGDAY', 'UPDATE_DATE', 'id']
    csv_file = "SHFE_Margin.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for d in dict_data:
                writer.writerow(d)
    except IOError:
        print("I/O error")

    # 处理csv文件，将列表统一成网页手动下载时的格式
    csv_data = pd.read_csv(csv_file, low_memory = False)
    csv_df = pd.DataFrame(csv_data)
    # 将列表的英文换成对应中文
    csv_df.columns = ['商品手续费率(%)', '交割手续费', '平今折扣率(%)', '合约代码', '投机买保证金率(%)', '结算价', '投机卖保证金率(%)', '套保买保证金率(%)', '套保卖保证金率(%)', '交易手续费率(%)', '交易手续费额(元/手)', '交易日', '更新日期', 'id']
    # 删掉手动下载格式中不存在的列
    csv_df.drop(csv_df.columns[[0, 11, 12, 13]], axis=1, inplace=True)
    # 重新排列列表的顺序
    csv_df = csv_df[['合约代码', '结算价', '交易手续费率(%)', '交易手续费额(元/手)', '交割手续费', '投机买保证金率(%)', '投机卖保证金率(%)', '套保买保证金率(%)', '套保卖保证金率(%)', '平今折扣率(%)']]
    csv_df = csv_df.set_index('合约代码')
    # 处理列表数据，更换保留位数及记录方式，将百分率转化成100为单位的百分比形式
    csv_df['结算价'] = csv_df['结算价'].astype(int)
    csv_df['交割手续费'] = csv_df['交割手续费'].astype(int)
    csv_df['交易手续费额(元/手)'] = csv_df['交易手续费额(元/手)'].astype(int)
    csv_df['交易手续费率(%)'] = csv_df['交易手续费率(%)']*1000
    csv_df['投机买保证金率(%)'] = (csv_df['投机买保证金率(%)']*100).astype(int)
    csv_df['投机卖保证金率(%)'] = (csv_df['投机卖保证金率(%)']*100).astype(int)
    csv_df['套保买保证金率(%)'] = (csv_df['套保买保证金率(%)']*100).astype(int)
    csv_df['套保卖保证金率(%)'] = (csv_df['套保卖保证金率(%)']*100).astype(int)
    csv_df['平今折扣率(%)'] = (csv_df['平今折扣率(%)']*100).astype(int)
    csv_df.to_csv(csv_file)

## 2.1 大连商品交易所
def dce_getForm():

    url1 = 'http://www.dce.com.cn/publicweb/businessguidelines/exportFutAndOptSettle.html?variety=all&trade_type=0&year='+year+'&month='+monthsub+'&day='+day0+'&exportFlag=excel'
    f1 = urlopen(url1) 
    data = f1.read() 
    with open("DCE_Margin.xls", "wb") as code:     
        code.write(data)

## 2.2 郑州商品交易所
def czce_getForm():

    # 示例下载链接2021-6-2: 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/2020/20200602/FutureDataClearParams.xls' 
    url2 = 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/'+year+'/'+year+month0+day0+'/FutureDataClearParams.xls' 
    f2 = urlopen(url2) 
    data = f2.read() 
    with open("CZCE_Margin.xls", "wb") as code:     
        code.write(data)

### 2.3 上海期货交易所
def shfe_getForm():
    
    # 示例下载链接2021-6-8: 'http://www.shfe.com.cn/data/instrument/Settlement20210608.dat' 
    url3 = 'http://www.shfe.com.cn/data/instrument/Settlement'+year+month0+day0+'.dat' 
    f3 = urlopen(url3) 
    data = f3.read().decode('utf-8')
    shfe_csvFile(data)

## 2.4 上海能源交易中心
def ine_getForm():

    # 示例下载链接2021-6-8日：'http://www.ine.cn/data/dailydata/js/js20210608.dat'
    url4 = 'http://www.ine.cn/data/dailydata/js/js'+year+month0+day0+'.dat' 
    f4 = urlopen(url4) 
    data = f4.read().decode('utf-8') 
    ine_csvFile(data)

## 2.5 中国金融期货交易所
def cffex_getForm():

    # 示例下载链接2021-5-28: 'http://www.cffex.com.cn/sj/jscs/202105/28/20210528_1.csv'
    url5 =  'http://www.cffex.com.cn/sj/jscs/202105/28/20210528_1.csv'
    f5 = urlopen(url5) 
    data = f5.read() 
    with open("CFFEX_Margin.csv", "wb") as code:     
        code.write(data)

### 下载全部5个网页最新的结算参数表格
def getAllForms():
    try:
        dce_getForm()
        czce_getForm()
        shfe_getForm()
        ine_getForm()
        cffex_getForm()
    except:
        print('May not be the right time to download.')

if __name__ == '__main__':
    getAllForms()