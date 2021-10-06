from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score,roc_curve
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import joblib
import time, datetime, os

# 设置系统时间为中国时区，用来输出每次训练完模型的时刻
os.environ['TZ'] = 'Asia/Shanghai'

class RFModel():

    def __init__(self, comm_type='', time_step=20, \
    predict_step=5, data_file=None, param_grid=None, \
    model_name=None, predict_data=None):

        self.comm_type = comm_type         # str，导入数据所属品种
        self.time_step = time_step         # 每time_step天作为一个整体预测未来趋势
        self.predict_step = predict_step   # 预测未来predict_step天的趋势
        self.data_file = data_file         # 训练模型的文件名
        self.model_name = model_name       # 加载模型的名字/训练后保存的模型名
        self.predict_data = predict_data   # 用来预测的数据指标
        self.dataframe = pd.DataFrame()    # 训练文件
        self.testframe = pd.DataFrame()    # 预测文件
        self.indicators = []               # 数据处理后的指标列表
        self.indicators_pred = []          # 用来预测的指标列表
        self.predict_cols = []             # 所有用来预测价格的指标
        self.x_train, self.x_test = None, None
        self.y_train, self.y_test = None, None
        self.X_set, self.y_set = None, None
        self.X_set_pred = None
        self.train_mode, self.predict_mode = False, False
        self.rfmodel = None    # 训练好的模型/加载出的模型
        self.param_grid = param_grid
        self.model_text = ''   # 保存的模型信息
        self.time = datetime.datetime.now()    # 保存模型的时刻


    # 如果用户没有输入param_grid的话就用默认参数
    def get_param_grid(self):

        if self.param_grid != None: return

        self.param_grid = {
            'criterion':['entropy','gini'],    # 两种评估分数的标准（损失函数）
            'max_depth':range(10, 110, 10),    # 深度：这里是森林中每棵决策树的深度，如果想自动生成深度的话用None
            'n_estimators':range(100, 400, 10),  # 决策树个数-随机森林特有参数
            'max_features':['auto', 'log2', 'sqrt'], # 每棵决策树使用的变量占比-随机森林特有参数（结合原理）
            'min_samples_split':range(2, 50, 2),  # 叶子的最小拆分样本量
            'random_state': range(0, 12, 1),   
            'class_weight': [None, 'balanced'],
            'min_samples_leaf': range(1, 30, 2)   # 叶子节点最少样本数
        }


    # 获取当前模式：训练模型/使用模型预测
    def get_mode(self):

        if self.data_file != None:
            self.train_mode = True
            print('Turn on training mode.')
        if self.predict_data != None:
            self.predict_mode = True
            print('Turn on predicting mode.')

    # 传入数据集、数据集的行数（已计算）、数据集里需用到的指标名称（英文，str形式）
    # dataframe: 数据集
    # n: 数据集的行数
    # params: 所有需要用到的指标参数名字列表
    def get_data(self):

        if self.train_mode:

            #获取数据集里收盘价一列数据, 中括号里面填收盘价的列名
            close_prices = self.dataframe.iloc[:, -1]
            # close_prices = dataframe['futures_settlement_price_iron_ore']

            #运用三种统计学计算方式处理收盘价
            n = len(self.dataframe)
            sma_data = RFModel.sma(self, close_prices, n)
            wma_data = RFModel.wma(self, close_prices, n)
            mom_data = RFModel.mom(self, close_prices, n)

            #添加处理后的收盘价列到原dataframe
            self.dataframe['sma'] = sma_data
            self.dataframe['wma'] = wma_data
            self.dataframe['mom'] = mom_data
            predict_cols = ['sma', 'wma', 'mom']

            #如果还输入了其他指标名称，则将整个列表延伸，纳入其余训练指标
            if self.indicators != []:
                predict_cols = predict_cols + self.indicators

            # 将指标存起来预测的时候用
            self.predict_cols = predict_cols

            #获取自变量集和因变量集，因变量为上涨/下跌（True=上涨，False=下跌）
            self.X_set = self.dataframe[predict_cols]
            #当前天与前一天价格相比，不变或者升高为上涨，下降为下跌
            self.y_set = list((close_prices.iloc[i] - close_prices.iloc[i-1])/close_prices.iloc[i-1] for i in list((range(1, n))))
            #因为第一天没有办法和前一天对比，所以默认涨幅为0，看作上涨
            self.y_set.insert(0, 0)

            self.model_text += ', '.join(predict_cols)
            self.model_text += '\n'
            self.model_text += '品种：' + self.comm_type + '\n'
            print(self.model_text)
        
        if self.predict_mode:

            #获取数据集里收盘价一列数据, 中括号里面填收盘价的列名
            close_prices = self.testframe.iloc[:, -1]
            # close_prices = dataframe['futures_settlement_price_iron_ore']

            #运用三种统计学计算方式处理收盘价
            n = len(self.testframe)
            sma_data = RFModel.sma(self, close_prices, n)
            wma_data = RFModel.wma(self, close_prices, n)
            mom_data = RFModel.mom(self, close_prices, n)

            #添加处理后的收盘价列到原dataframe
            self.testframe['sma'] = sma_data
            self.testframe['wma'] = wma_data
            self.testframe['mom'] = mom_data

            #获取自变量集和因变量集，因变量为上涨/下跌（True=上涨，False=下跌）
            self.X_set_pred = self.testframe[self.indicators_pred]


    # simple moving average五日平均计算
    def sma(self, close_prices, n):

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
    def wma(self, close_prices, n):

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
    def mom(self, close_prices, n):

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
    def clean_columns(self):

        if self.train_mode:

            all_null = dict(self.dataframe.isnull().sum())
            data_col = len(self.dataframe)
            dump = []
            for key, value in all_null.items():
                print(value/data_col)
                if value/data_col >= 0.20:
                    dump.append(key)
            if dump != []:
                self.dataframe.drop(dump, axis=1)

        if self.predict_mode:

            all_null = dict(self.testframe.isnull().sum())
            data_col = len(self.testframe)
            dump = []
            for key, value in all_null.items():
                print(value/data_col)
                if value/data_col >= 0.20:
                    dump.append(key)
            if dump != []:
                self.testframe.drop(dump, axis=1)


    # 调参，绘制学习曲线来调参 n_estimators对随机森林影响最大
    def param_adjust(self):

        print('Start adjusting parameters.')

        # 获取param_grid调试参数
        RFModel.get_param_grid(self)

        gsearch = GridSearchCV(estimator = RandomForestClassifier(), 
        param_grid=self.param_grid, scoring='roc_auc', cv=5)
        gsearch.fit(self.x_train, self.y_train)
        print(gsearch.best_params_, gsearch.best_score_)
        
        self.best_params = gsearch.best_params_

        print('Finished adjusting parameters.')


    # True=上涨，False=下跌
    def predict_price(self):

        y_predict = self.rfmodel.predict(self.X_set_pred)
        
        if y_predict:
            print(self.testframe.columns.tolist()[-4], ":", "预计未来%d天呈上涨趋势" % self.predict_step)
        else:
            print(self.testframe.columns.tolist()[-4], ":", "预计未来%d天呈下降趋势" % self.predict_step)


    # 计算特征相关性并剔除相关性高于80%的变量（保留一个）
    def clean_relation(self):

        if not self.train_mode: return

        data = self.dataframe.iloc[:,1:-1]  #取数据中指标所在的列
        data = data.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))  #归一化
        cor = data.corr()  #选取部分特征计算
        cor = cor.drop(cor[cor.iloc[:,0]>0.8].index)
        rows = cor._stat_axis.values.tolist()
        columns = cor.columns.values.tolist()

        self.indicators = rows + [columns[0]]


    # 将dataframe里面所有列的类型都转化为float，方便后续进行模型训练
    def to_num(self):

        if self.train_mode:
            cols = self.dataframe.columns
            for col in cols:
                if not isinstance(self.dataframe[col].dtype, float):
                    self.dataframe[col] = self.dataframe[col].apply(pd.to_numeric, errors='coerce')

        if self.predict_mode:
            cols = self.testframe.columns
            for col in cols:
                if not isinstance(self.testframe[col].dtype, float):
                    self.testframe[col] = self.testframe[col].apply(pd.to_numeric, errors='coerce')


    # 处理集合，变成用time_step天前的数据来进行预测
    def organize_sets(self):

        if self.train_mode:

            # x_set：二维数组, len=3409, 每个element=17
            x_set, y_set = pd.DataFrame(self.X_set).values, pd.DataFrame(self.y_set).values

            train_x = [x_set[i:i+self.time_step] for i in range(x_set.shape[0])]
            train_y = [y_set[i:i+self.predict_step] for i in range(y_set.shape[0])]

            train_x, train_y = np.array(train_x, dtype=object), np.array(train_y, dtype=object)

            train_x, train_y = RFModel.help_clean_array(train_x, False), RFModel.help_clean_array(train_y, True)

            train_y = np.ravel(train_y)
            
            self.X_set, self.y_set = train_x, train_y


        if self.predict_mode:

            x_set = pd.DataFrame(self.X_set_pred).values

            pred_list = list()

            # 将所有天数据取平均数处理，最后每个指标只对应一个值
            for i in range(x_set.shape[1]):
                mean_data = sum(x_set[j][i] for j in range(x_set.shape[0]))/x_set.shape[0]
                pred_list.append(mean_data)

            self.X_set_pred = np.array(pred_list).reshape(1, -1)


    # 将三维训练数组转化为二维，取平均值
    # 如果是因变量集合则需要转化为true/false二分结果，其中
    # true=上涨，false=下跌    
    def help_clean_array(train_data, is_y):

        result = list()

        for arr in train_data:
            total_1d = len(arr)
            total_cols = len(arr[0])
            temp_list = list()
            for i in range(total_cols):
                mean_data = sum(arr[j][i] for j in range(total_1d))/total_1d
                # 判断是否是因变量训练集
                if is_y:
                    temp_list.append(mean_data >= 0)
                else:
                    temp_list.append(mean_data)
            result.append(temp_list)

        return np.array(result)


    # 加载已保存的模型
    def load_model(self):

        if self.model_name == None: 
            print("model_name doesn't exist")
            return

        start = time.time()
        model = joblib.load(self.model_name)
        end = time.time()
        print('模型加载时间 : %s 秒'%(end-start))
       
        self.rfmodel = model

        name, suffix = self.model_name.split('.')
        with open(name + '.txt', 'r') as f:
            print(f.read())

        predict_cols = ''
        text_file = open(name + '.txt', 'r')
        for text in text_file:
            if text.find('品种') != -1:
                break
            predict_cols += text

        # 获取所有要用到的指标
        self.indicators_pred = predict_cols[:-1].split(', ')

        for text in text_file:
            if text.find('天为单位训练') != -1:
                i1 = text.index('以')
                i2 = text.index('天为单位训练')
                self.time_step = int(text[i1+1:i2])
            if text.find('天的趋势') != -1:
                i1 = text.index('预测未来')
                i2 = text.index('天的趋势')
                self.predict_step = int(text[i1+4:i2])
        
    
    # 评估模型的准确率
    def evaluate_model(self):

        importance = self.rfmodel.feature_importances_
        imp_res = dict()
        for i, name in enumerate(self.predict_cols):
            imp_res[name] = str(round(importance[i]*100, 2)) + '%'

        print("特征重要性：")
        print(str(imp_res))

        y_predict = self.rfmodel.predict(self.x_test)
        report = metrics.precision_recall_fscore_support(y_predict, self.y_test)
        col_name = ['精确率', '召回率', 'f1分数', '样本数']
        row_name = ['下跌', '上涨']
        res_df = pd.DataFrame(np.zeros((2, 4)), index=row_name, columns=col_name, dtype=int)
        for c in [0, 1, 2, 3]:
            for r in [0, 1]:
                if c == 3:
                    res_df.loc[row_name[r], col_name[c]] = report[c][r]
                else:
                    res_df.loc[row_name[r], col_name[c]] = str(round(report[c][r]*100, 2)) + '%'
        print(res_df)

        fpr_test, tpr_test, th_test = metrics.roc_curve(y_predict, self.y_test)
        auc = round(metrics.auc(fpr_test, tpr_test)*100, 2)
        print('精确度AUC :', str(auc), '%')

        score = round(np.mean(cross_val_score(self.rfmodel,self.X_set,self.y_set,cv=5,scoring='accuracy'))*100, 2)
        print('交叉验证得分：'+str(score)+ '%')
        print(self.time)

        y_predict = self.rfmodel.predict_proba(self.x_test)
        fpr,tpr,theta = roc_curve(self.y_test,y_predict[:,-1])

        self.model_text +=  "特征重要性："+ '\n' + str(imp_res) + '\n' + '随机森林性能表：' + '\n' + str(res_df) + '\n' + '精确度AUC：' + str(auc) + '%' + '\n' + '交叉验证得分：' + str(score) + '%'

        #画出ROC曲线
        # plt.plot(fpr,tpr)
        # plt.show()


    # 读取数据集并转化为可以训练的
    def clean_dataframe(self):

        if self.train_mode:

            self.dataframe = pd.read_excel(self.data_file)
            print(self.dataframe.head())

            # 将dataframe里面所有非float类型的数据转化成float类型
            RFModel.to_num(self)

            # 线性填充缺失值
            self.dataframe.interpolate(method='values', inplace=True)
            # 剩余无法线性填充的用前后数据进行填充
            self.dataframe.fillna(method='ffill', inplace=True)
            self.dataframe.fillna(method='bfill', inplace=True)


        if self.predict_mode:

            self.testframe = pd.read_excel(self.predict_data)
            print(self.testframe.head())

            # 将dataframe里面所有非float类型的数据转化成float类型
            RFModel.to_num(self)

            # 线性填充缺失值
            self.testframe.interpolate(method='values', inplace=True)
            # 剩余无法线性填充的用前后数据进行填充
            self.testframe.fillna(method='ffill', inplace=True)
            self.testframe.fillna(method='bfill', inplace=True)

        #随机森林建模
        #清理一下相关性高的指标，获得最终传入模型的指标list
        RFModel.clean_relation(self)
        print('Finished cleaning data.')


    # 获取训练集和测试集
    def get_data_sets(self):
        
        if not self.train_mode: return

        RFModel.get_data(self)
        RFModel.organize_sets(self)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.X_set, self.y_set, test_size=0.2, random_state=12345)
        print('Finished splitting data sets.')

    
    # 随机森林模型训练
    def train_model(self):

        if not self.train_mode: return

        RFModel.param_adjust(self)

        print('Start training.')

        model = RandomForestClassifier(criterion=self.best_params['criterion'], 
        class_weight=self.best_params['class_weight'], n_estimators=self.best_params['n_estimators'], min_samples_split=self.best_params['min_samples_split'], min_samples_leaf=self.best_params['min_samples_leaf'], max_depth=self.best_params['max_depth'], max_features=self.best_params['max_features'], random_state=self.best_params['random_state'], n_jobs = -1, oob_score = True)
        model.fit(self.x_train, self.y_train)

        # model = RandomForestClassifier(criterion='entropy', class_weight='balanced', n_estimators=900, min_samples_split=300, min_samples_leaf=100, max_depth=20, max_features=7, random_state=4)
        # model.fit(self.x_train, self.y_train)

        self.rfmodel = model


    # 将训练好的模型保存到当前文件夹
    def save_model(self):

        if self.rfmodel == None:
            print('No model to save')
            return

        print("Start saving model and model info.")
        #如果用户没有输入模型保存的名字的话，就默认保存为rf_model.m
        if self.model_name == None:
            self.model_name = self.data_file + '_model.m'
        joblib.dump(self.rfmodel, self.model_name)

        self.model_text += '\n' + str(self.time) + '\n'
        self.model_text += str(self.best_params) + '\n'
        self.model_text += '以%d天为单位训练' % self.time_step + '\n'
        self.model_text += '预测未来%d天的趋势' % self.predict_step
        print('以%d天为单位训练' % self.time_step)
        print('预测未来%d天的趋势' % self.predict_step)

        name, suffix = self.model_name.split('.')
        with open(name+'.txt', 'w') as f:
            f.write(self.model_text)
        print("Finished saving model and model info.")


    def run_train_process(self):

        # 获取运行模式
        RFModel.get_mode(self)
        # 载入数据集并进行处理，方便后续训练模型
        RFModel.clean_dataframe(self)
        # 获取训练集和测试集
        RFModel.get_data_sets(self)
        # 训练模型
        RFModel.train_model(self)


    def run_predict_process(self):

        RFModel.get_mode(self)
        # 加载当前储存的模型
        RFModel.load_model(self)
        # 载入数据集并进行处理，方便后续使用模型进行预测
        RFModel.clean_dataframe(self)
        RFModel.get_data(self)
        RFModel.organize_sets(self)
        
        print(self.time)
        RFModel.predict_price(self)


    # 若想单独检测模型的性能，则需要自己输入测试数据
    def run_evaluate_process(self):

        if self.train_mode:
            RFModel.evaluate_model(self)
        else:
            try:
                # 加载输入的模型
                RFModel.load_model(self)
                RFModel.evaluate_model(self)
            except:
                print('Cannot evaluate this model')

if __name__ == '__main__':

    param_grid = {
            'criterion':['gini'],
            'max_depth':range(10, 30, 10),    # 深度：这里是森林中每棵决策树的深度，如果想自动生成深度的话用None
            'n_estimators':range(100, 140, 10),  # 决策树个数-随机森林特有参数
            'max_features':['auto', 'log2'], # 每棵决策树使用的变量占比-随机森林特有参数（结合原理）
            'min_samples_split':range(4, 6, 2),  # 叶子的最小拆分样本量
            'random_state': range(4, 6, 1),
            'class_weight': ['balanced'],
            'min_samples_leaf': range(1, 4, 2)
        }

    # 创建一个随机森林project

    # 更改这个就行，True为训练模式，False为预测模式
    do_train = False
    
    if do_train:
        RF = RFModel('钢材', 20, 5, '钢材_清理.xlsx', param_grid, 'steel_new.m')

        # 训练一个随机森林模型
        RF.run_train_process()

        RF.run_evaluate_process()

        # 将训练完的模型保存到当前文件夹内
        RF.save_model()

    else:

        RF = RFModel('钢材', None, None, None, None, 'steel_new.m', '钢材_预测.xlsx')

        RF.run_predict_process()

    