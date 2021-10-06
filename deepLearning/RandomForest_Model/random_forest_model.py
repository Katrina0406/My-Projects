
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score,roc_curve
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 传入数据集、数据集的行数（已计算）、数据集里需用到的指标名称（英文，str形式）
# dataframe: 数据集
# n: 数据集的行数
# params: 所有需要用到的指标参数名字列表
def get_prediction_data(dataframe, n, params):

    #获取数据集里收盘价一列数据, 中括号里面填收盘价的列名
    close_prices = dataframe['futures_settlement_price_rebar']
    #铁矿石数据集用这个：
    # close_prices = dataframe['futures_settlement_price_iron_ore']

    #运用三种统计学计算方式处理收盘价
    sma_data = sma(close_prices, n)
    wma_data = wma(close_prices, n)
    mom_data = mom(close_prices, n)

    #添加处理后的收盘价列到原dataframe
    dataframe['sma'] = sma_data
    dataframe['wma'] = wma_data
    dataframe['mom'] = mom_data
    predict_cols = ['sma', 'wma', 'mom']

    #如果还输入了其他指标名称，则将整个列表延伸，纳入其余训练指标
    if params != []:
        predict_cols = predict_cols + params

    #获取自变量集和因变量集，因变量为上涨/下跌（True=上涨，False=下跌）
    X_set = dataframe[predict_cols]
    #当前天与前一天价格相比，不变或者升高为上涨，下降为下跌
    y_set = list(close_prices.iloc[i] >= close_prices.iloc[i-1] for i in list((range(1, n))))
    #因为第一天没有办法和前一天对比，所以默认涨幅为0，看作上涨
    y_set.insert(0, True)

    return X_set, y_set

# simple moving average五日平均计算
def sma(close_prices, n):
    sma_col = list()
    for i in range(n):
        if i == 0:
            sma_value = close_prices.iloc[0]
        elif i == 1:
            sma_value = (close_prices.iloc[0]+close_prices.iloc[1])/2
        elif i == 2:
            sma_value = (close_prices.iloc[0]+close_prices.iloc[1]+close_prices.iloc[2])/3
        elif i == 3:
            sma_value = (close_prices.iloc[0]+close_prices.iloc[1]+close_prices.iloc[2]+close_prices.iloc[3])/3
        else:
            sma_value = (close_prices.iloc[i] + close_prices.iloc[i-1] + close_prices.iloc[i-2] + close_prices.iloc[i-3] + close_prices.iloc[i-4]) / 5
        sma_col.append(sma_value)
    return sma_col

# weighted moving average加权平均计算
def wma(close_prices, n):
    wma_col = list()
    wma_col.append(close_prices.iloc[0])
    for i in range(1, n):
        nomi = deno = 0
        for j in range(0, i+1, 2):
            if j != i:
                nomi += (close_prices.iloc[j] + close_prices.iloc[j+1]) * (j+1)
            else:
                nomi += close_prices.iloc[j] * 2 * (j+1)
            deno += 2 * (j+1)
        wma_value = nomi / deno
        wma_col.append(wma_value)
    return wma_col

# momentum 当日收盘价-12天前收盘价计算
def mom(close_prices, n):
    mom_col = list()
    for i in range (n):
        if i < 12:
            mom_col.append(0)
        else:
            delta = close_prices.iloc[i] - close_prices.iloc[i-12]
            mom_col.append(delta)
    return mom_col

# 清除掉缺失值占总数据20%以上的数据列
# 仅用于都是每日数据的数据集，每月数据不适用因为本身就一个月只有一天有数据（因此会有大量空缺）
# 所以一般含月数据的数据集自行手动清理判断
def clean_columns(dataframe):
    all_null = dict(dataframe.isnull().sum())
    data_col = len(dataframe)
    dump = []
    for key, value in all_null.items():
        print(value/data_col)
        if value/data_col >= 0.20:
            dump.append(key)
    if dump != []:
        dataframe.drop(dump, axis=1)
    return dataframe

def param_adjust(x_train, y_train):
    # 调参，绘制学习曲线来调参n_estimators（对随机森林影响最大）
    score_lt = []

    # 每隔10步建立一个随机森林，获得不同n_estimators的得分
    for i in range(0,200,10):
        rfc = RandomForestClassifier(n_estimators=i+1
                                    ,random_state=90)
        score = cross_val_score(rfc, x_train, y_train, cv=10).mean()
        score_lt.append(score)
        score_max = max(score_lt)
    print('最大得分：{}'.format(score_max),
        '子树数量为：{}'.format(score_lt.index(score_max)*10+1))

    # 绘制学习曲线
    x = np.arange(1,201,10)
    plt.subplot(111)
    plt.plot(x, score_lt, 'r-')
    plt.show()

# 输入想预测的日期，输出结果是上涨还是下跌
# 仅用于GridSearchCV生成的随机森林模型（第二种）
def predict(x_predict, model, multi):
    y_predict = model.best_estimator_.predict(x_predict)
    if not multi:
        if y_predict:
            return (x_predict, "预计上涨")
        else:
            return (x_predict, "预计下跌")
    else:
        result = []
        for y in y_predict:
            if y:
                result.append("预计上涨")
            else:
                result.append("预计下跌")
        return (x_predict, result)

# 仅用于第一个模型（只用到随机森林分类器）
# True=上涨，False=下跌
def predict_price(model, x_test):
    result = model.predict(x_test)
    return result

# 计算特征相关性并剔除相关性高于80%的变量（保留一个）
def clean_relation(dataframe):

    data = dataframe.iloc[:,1:-1]  #取数据中指标所在的列
    data = data.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))  #归一化
    cor = data.corr()  #选取部分特征计算
    # cor.to_csv('relation.csv')
    cor = cor.drop(cor[cor.iloc[:,0]>0.8].index)
    rows = cor._stat_axis.values.tolist()
    columns = cor.columns.values.tolist()

    return rows + [columns[0]]

# 将dataframe里面所有列的类型都转化为float，方便后续进行模型训练
def to_num(df):

    cols = df.columns
    for col in cols:
        if not isinstance(df[col].dtype, float):
            df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    
    return df


if __name__ == '__main__':

    df = pd.read_excel("steel_clean.xlsx")
    # df = pd.read_excel("iron_ore.xlsx")

    # 将dataframe里面所有非float类型的数据转化成float类型
    df = to_num(df)

    # 线性填充缺失值
    
    df.interpolate(method='values', inplace=True)
    # 剩余无法线性填充的用前后数据进行填充
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    #随机森林建模
    #清理一下相关性高的指标，获得最终传入模型的指标list
    params = clean_relation(df)
    X_set, y_set = get_prediction_data(df, len(df), params)
    x_train, x_test, y_train, y_test = train_test_split(X_set, y_set, test_size=0.2, random_state=12345)

    #生成并使用随机模型 2种写法，略微不同但大致效果一致
    ########################################################################

    #1 不用网格搜索
    model = RandomForestClassifier(criterion='entropy', class_weight='balanced', n_estimators=900, min_samples_split=300, min_samples_leaf=100, max_depth=20, max_features=7, random_state=4)
    model.fit(x_train, y_train)

    score = np.mean(cross_val_score(model,x_test,y_test,cv=5,scoring='accuracy'))
    print('平均性能得分：'+str(score))
    print("特征重要性："+str(model.feature_importances_))
    y_predict = model.predict(x_test)
    test_est = model.predict(x_test)
    print('随机森林精确度：')
    print(metrics.classification_report(test_est, y_test))
    print('随机森林 AUC：')
    fpr_test, tpr_test, th_test = metrics.roc_curve(test_est, y_test)
    print('AUC = %.4f'%metrics.auc(fpr_test, tpr_test))

    ################################################################

    # 2 用网格搜索
    param_grid = {
        'criterion': ['entropy'],
        'max_depth': [90],    # 深度：这里是森林中每棵决策树的深度
        'n_estimators': [800],  # 决策树个数-随机森林特有参数
        'max_features': [7], # 每棵决策树使用的变量占比-随机森林特有参数（结合原理）
        'min_samples_split': [300],  # 叶子的最小拆分样本量
        'min_samples_leaf': [100],
        'class_weight': ['balanced'],
        'random_state':[4]
    }

    rfc = RandomForestClassifier()
    rfc_model = GridSearchCV(estimator=rfc, param_grid=param_grid, scoring='roc_auc', cv=5)
    rfc_model.fit(x_train, y_train)

    # 测试模型的得分（三种方式）
    print("roc_auc_score: ")
    print(roc_auc_score(y_test, rfc_model.best_estimator_.predict_proba(x_test)[:, 1]))
    score = cross_val_score(rfc, x_test, y_test, cv=5).mean()
    print("cross validation score:", score)
    print("model best score:", rfc_model.best_score_)

    # 预测某一天的价格趋势
    x_predict = x_test[-1:]
    print(predict(x_predict, rfc_model, 1))
    # 预测某几天的价格趋势
    x_predict_list = x_test[-3:]
    print(predict(x_predict_list, rfc_model, 3))

    test_est2 = rfc_model.predict(x_test)
    print('随机森林精确度2：')
    print(metrics.classification_report(test_est2, y_test))
    print('随机森林 AUC 2：')
    fpr_test, tpr_test, th_test = metrics.roc_curve(test_est2, y_test)
    print('AUC = %.4f'%metrics.auc(fpr_test, tpr_test))


    y_predict = rfc_model.predict_proba(x_test)
    fpr,tpr,theta = roc_curve(y_test,y_predict[:,-1])
    #画出ROC曲线
    plt.plot(fpr,tpr)
    plt.show()

    ########################################################################



    
