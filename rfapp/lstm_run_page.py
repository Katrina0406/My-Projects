import numpy as np
import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from LSTM_model import train, predict
import pandas as pd

frame = "pytorch"

class Config:

    def __init__(self, comm_type, time_s, predict_d, total_cols, model_name, lstm_layer, dropout_rate, batch_size, learning_rate, hidden_size, epoch, patience, do_train, train_data=None, predict_data=None):

        self.comm_type = comm_type
        # 数据参数
        self.feature_columns = list(range(1, total_cols))    # 要作为feature的列，按原数据从0开始计算，也可以用list 如 [2,4,6,8] 设置
        self.label_columns = [total_cols-1]               # 要预测的列，按原数据从0开始计算, 默认最后一列为收盘价，即预测列
        self.label_in_feature_index = (lambda x,y: [x.index(i) for i in y])(self.feature_columns, self.label_columns)  # 因为feature不一定从0开始

        # 网络参数
        self.input_size = len(self.feature_columns)
        self.output_size = len(self.label_columns)

        self.hidden_size = hidden_size            # LSTM的隐藏层大小，也是输出大小
        self.lstm_layers = lstm_layer            # LSTM的堆叠层数
        self.dropout_rate = dropout_rate         # dropout概率
        self.time_step = time_s             # 这个参数很重要，是设置用前多少天的数据来预测，也是LSTM的time step数
        self.predict_day = predict_d            # 预测未来几天

        self.picturename = '(Tech_Coal_Classifier_temp)'

        # 训练参数
        self.do_train = do_train
        self.add_train = False           # 是否载入已有模型参数进行增量训练
        self.shuffle_train_data = True   # 是否对训练数据做shuffle
        self.use_cuda = False            # 是否使用GPU训练

        self.train_data_rate = 0.9      # 训练数据占总体数据比例，测试数据就是 1-train_data_rate
        self.valid_data_rate = 0.1      # 验证数据占训练数据比例，验证集在训练过程使用，为了做模型和参数选择

        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.epoch = epoch                 # 整个训练集被训练多少遍，不考虑早停的前提下
        self.patience = patience                # 训练多少epoch，验证集没提升就停掉
        self.random_seed = 42            # 随机种子，保证可复现

        self.do_continue_train = False    # 每次训练把上一次的final_state作为下一次的init_state
        self.continue_flag = ""           # 但实际效果不佳，可能原因：仅能以 batch_size = 1 训练
        if self.do_continue_train:
            shuffle_train_data = False
            batch_size = 1
            continue_flag = "continue_"

        # 训练模式
        self.debug_mode = False  # 调试模式下，是为了跑通代码，追求快
        self.debug_num = 500  # 仅用debug_num条数据来调试

        # 框架参数
        self.used_frame = frame
        self.model_postfix = {"pytorch": ".pth"}
        self.model_name = model_name

        # 路径参数
        self.train_data_path = train_data
        self.predict_data_path = predict_data
        self.model_save_path = r"DeepLearning/" + self.model_name + "/"
        self.figure_save_path = r"DeepLearning/"
        self.log_save_path = r"DeepLearning/"
        self.do_log_print_to_screen = True
        self.do_log_save_to_file = True
        self.do_figure_save = True
        self.do_train_visualized = False

        if not os.path.exists(self.model_save_path):
            os.makedirs(self.model_save_path)
        if not os.path.exists(self.figure_save_path):
            os.mkdir(self.figure_save_path)
        if self.do_train and (self.do_log_save_to_file or self.do_train_visualized):
            cur_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
            log_save_path = self.log_save_path + cur_time + '_' + self.used_frame + "/"
            os.makedirs(log_save_path)


class Data:
    def __init__(self, config):
        self.config = config
        self.data, self.data_column_name = self.read_data()

        self.data_num = self.data.shape[0]
        self.train_num = int(self.data_num * self.config.train_data_rate)

        self.mean = np.nanmean(self.data, axis=0)              # 数据的均值和方差
        self.std = np.nanstd(self.data, axis=0)
        self.norm_data = (self.data - self.mean)/self.std   # 归一化，去量纲

        self.start_num_in_test = 0      # 测试集中前几天的数据会被删掉，因为它不够一个time_step

    # 将dataframe里面所有列的类型都转化为float，方便后续进行模型训练
    def to_num(df):
        cols = df.columns
        for col in cols:
            if not isinstance(df[col].dtype, float):
                df[col] = df[col].apply(pd.to_numeric, errors='coerce')
        
        return df     

    # 清理数据，填充缺失值
    def clean_data(dataframe):
        dataframe = Data.to_num(dataframe)
        dataframe.interpolate(method='values', inplace=True)
        dataframe.fillna(method='ffill', inplace=True)
        dataframe.fillna(method='bfill', inplace=True)

        return dataframe

    # 读取数据集数据
    def read_data(self):                # 读取初始数据
        if self.config.do_train:
            if self.config.debug_mode:
                init_data = pd.read_excel(self.config.train_data_path, nrows=self.config.debug_num, usecols=self.config.feature_columns)
                init_data = Data.clean_data(init_data)
            else:
                init_data = pd.read_excel(self.config.train_data_path, usecols=self.config.feature_columns)
                init_data = Data.clean_data(init_data)
        else:
            init_data = pd.read_excel(self.config.predict_data_path, usecols=self.config.feature_columns)
            init_data = Data.clean_data(init_data)
            
        return init_data.values, init_data.columns.tolist()     # .columns.tolist() 是获取列名

    # 获取用来训练和验证的数据集
    def get_train_and_valid_data(self):
        if not self.config.do_train: return
        feature_data = self.norm_data[:self.train_num]
        label_data = self.norm_data[self.config.predict_day : self.config.predict_day + self.train_num,
                                    self.config.label_in_feature_index]    # 将延后几天的数据作为label

        if not self.config.do_continue_train:
            # 在非连续训练模式下，每time_step行数据会作为一个样本，两个样本错开一行，比如：1-20行，2-21行。。。。
            train_x = [feature_data[i:i+self.config.time_step] for i in range(self.train_num-self.config.time_step)]
            train_y = [label_data[i:i+self.config.time_step] for i in range(self.train_num-self.config.time_step)]
        else:
            train_x = [feature_data[start_index + i*self.config.time_step : start_index + (i+1)*self.config.time_step]
                       for start_index in range(self.config.time_step)
                       for i in range((self.train_num - start_index) // self.config.time_step)]
            train_y = [label_data[start_index + i*self.config.time_step : start_index + (i+1)*self.config.time_step]
                       for start_index in range(self.config.time_step)
                       for i in range((self.train_num - start_index) // self.config.time_step)]

        train_x, train_y = np.array(train_x), np.array(train_y)

        train_x, valid_x, train_y, valid_y = train_test_split(train_x, train_y, test_size=self.config.valid_data_rate,
                                                              random_state=self.config.random_seed,
                                                              shuffle=self.config.shuffle_train_data)   # 划分训练和验证集，并打乱
        return train_x, valid_x, train_y, valid_y

    # 获取测试集/预测集
    def get_test_data(self, return_label_data=False):
        if self.config.do_train:
            feature_data = self.norm_data[self.train_num:]
        else:
            feature_data = self.norm_data
        self.start_num_in_test = feature_data.shape[0] % self.config.time_step  # 这些天的数据不够一个time_step
        time_step_size = feature_data.shape[0] // self.config.time_step

        # 在测试数据中，每time_step行数据会作为一个样本，两个样本错开time_step行
        # 比如：1-20行，21-40行。。。到数据末尾。
        test_x = [feature_data[self.start_num_in_test+i*self.config.time_step : self.start_num_in_test+(i+1)*self.config.time_step]
                for i in range(time_step_size)]
        if return_label_data:       # 实际应用中的测试集是没有label数据的
            if self.config.do_train:
                label_data = self.norm_data[self.train_num + self.start_num_in_test:, self.config.label_in_feature_index]
            else:
                label_data = self.norm_data[self.start_num_in_test:, self.config.label_in_feature_index]
            return np.array(test_x), label_data
        
        return np.array(test_x)

# 保存模型信息
def load_logger(config):
    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)

    # StreamHandler
    if config.do_log_print_to_screen:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level=logging.INFO)
        formatter = logging.Formatter(datefmt='%Y/%m/%d %H:%M:%S',
                                      fmt='[ %(asctime)s ] %(message)s')
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    # FileHandler
    if config.do_log_save_to_file:
        file_handler = RotatingFileHandler(config.log_save_path + "out.log", maxBytes=1024000, backupCount=5)
        file_handler.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 把config信息也记录到log 文件中
        config_dict = {}
        for key in dir(config):
            if not key.startswith("_"):
                config_dict[key] = getattr(config, key)
        config_str = str(config_dict)
        config_list = config_str[1:-1].split(", '")
        config_save_str = "\nConfig:\n" + "\n'".join(config_list)
        logger.info(config_save_str)

    return logger

# 格式化输出模型运行结果
def draw(config: Config, origin_data: Data, logger, predict_norm_data: np.ndarray):
    if not config.do_train:
        label_data = origin_data.data[origin_data.start_num_in_test : ,
                                                config.label_in_feature_index]
    else:
        label_data = origin_data.data[origin_data.train_num + origin_data.start_num_in_test : ,
                                            config.label_in_feature_index]
    predict_data = predict_norm_data * origin_data.std[config.label_in_feature_index] + \
                   origin_data.mean[config.label_in_feature_index]   # 通过保存的均值和方差还原数据
    
    assert label_data.shape[0]==predict_data.shape[0], "The element number in origin and predicted data is different"

    label_name = [origin_data.data_column_name[i] for i in config.label_in_feature_index]
    label_column_num = len(config.label_columns)

    loss = np.mean((label_data[config.predict_day:] - predict_data[:-config.predict_day] ) ** 2, axis=0)
    loss_norm = loss/(origin_data.std[config.label_in_feature_index] ** 2)
    logger.info("{} 的均方误差为 ".format(label_name) + str(loss_norm))

    if config.do_train:
        label_X = range(origin_data.data_num - origin_data.train_num - origin_data.start_num_in_test)
    else:
        label_X = range(origin_data.data_num - origin_data.start_num_in_test)
    predict_X = [ x + config.predict_day for x in label_X]

    # 0.2以上为上涨，用2表示
    # -0.2-0.2为震荡，用1表示
    # -0.2以下为下跌，用0表示
    for i in range(label_column_num):
        new_data = predict_data
        if i == 0:
            predict_data[:, i] = 1
        elif abs(new_data[:, i] - new_data[:, i-1]) < 0.2:
            predict_data[:, i] = 1
        elif new_data[:, i] > new_data[:, i-1]:
            predict_data[:, i] = 2
        else:
            predict_data[:, i] = 0

        plt.figure(i+1)                     # 预测数据绘制
        plt.plot(label_X, label_data[:, i], label='label')
        plt.plot(predict_X, predict_data[:, i], label='predict')

        label = predict_data[-config.predict_day:, i]
        label_print = []
        for sign in label:
            if sign == 1:
                label_print.append('震荡')
            elif sign == 0:
                label_print.append('下跌')
            else:
                label_print.append('上涨')

        plt.title("LSTM {} 在 {} 的表现是".format(config.picturename,label_name[i]))
        logger.info("预测列 {} 在未来 {} 天的趋势是: ".format(label_name[i], config.predict_day) +
                str(np.squeeze(label_print)))
        if config.do_figure_save:
            plt.savefig(config.figure_save_path+"{}predict_{}_with_{}.png".format(config.continue_flag, label_name[i], config.picturename))

def ROC(config: Config, origin_data: Data, predict_norm_data: np.ndarray):
    label_data = origin_data.data[origin_data.train_num + origin_data.start_num_in_test : ,
                                            config.label_in_feature_index]
    predict_data = predict_norm_data * origin_data.std[config.label_in_feature_index] + \
                   origin_data.mean[config.label_in_feature_index]   # 通过保存的均值和方差还原数据
    assert label_data.shape[0]==predict_data.shape[0], "The element number in origin and predicted data is different"

    #转化原始价格集和预测价格集，生成两个list
    #list里面0代表下跌，1代表震荡，2代表上涨
    def get_result(origin_data, predict_data):
            origin, predict = [], []
            for i in range(1, len(origin_data)):
                if abs(origin_data[i] - origin_data[i-1]) < 0.2:
                    origin.append(1)
                elif origin_data[i] > origin_data[i-1]:
                    origin.append(2)
                else:
                    origin.append(0)
            for i in range(1, len(predict_data)):
                if abs(predict_data[i] - predict_data[i-1]) < 0.2:
                    predict.append(1)
                elif predict_data[i] > predict_data[i-1]:
                    predict.append(2)
                else:
                    predict.append(0)
            return origin, predict

    label_name = [origin_data.data_column_name[i] for i in config.label_in_feature_index]
    label_column_num = len(config.label_columns)

    label_data, predict_data = get_result(label_data, predict_data)

    for i in range(label_column_num):

        point_prediction = pd.DataFrame([label_data, predict_data], index=['reallabel', 'predlabel']).transpose()
        # 3 classes statistics
        def triple_class_accuracy(df):
            index_name = ['实际下跌', '实际震荡', '实际上涨']
            col_name = ['判跌', '判震荡', '判涨']
            res_df = pd.DataFrame(np.zeros((3, 3)), index=index_name, columns=col_name, dtype=int)
            # N = df.shape[0]
            for r in [-1, 0, 1]:
                for c in [-1, 0, 1]:
                    res_df.loc[index_name[r + 1], col_name[c + 1]] = (
                            (df['reallabel'] == r + 1) & (df['predlabel'] == c + 1)).sum()
            return res_df

        winning_sample = np.trace(triple_class_accuracy(point_prediction))
        resMatrix = triple_class_accuracy(point_prediction)

        print(resMatrix)
        # 严趋势判准率:（下跌判下跌+震荡判震荡+上涨判上涨）/所有
        print('严趋势判准率:{:.2f}%'.format(100 * np.trace(resMatrix) / point_prediction.shape[0]))
        # 松弛趋势判准率: （下跌判下跌+震荡判震荡+上涨判上涨+下跌判震荡+上涨判震荡）/所有
        print('松弛趋势判准率:{:.2f}%'.format(
            100 * (np.trace(resMatrix) + 0.5 * resMatrix.values[2][1] + 0.5 * resMatrix.values[0][1]) /
            point_prediction.shape[0]))

        plt.figure()                     # 预测数据绘制
        TPR = [0]
        FPR = [0]
        negative_num = point_prediction.shape[0] - winning_sample
        for k in range(point_prediction.shape[0]):
            if point_prediction.iloc[k, 0] == point_prediction.iloc[k, 1]:
                TPR.append(TPR[-1] + 1 / winning_sample)
                FPR.append(FPR[-1])
            else:
                FPR.append(FPR[-1] + 1 / negative_num)
                TPR.append(TPR[-1])
        plt.plot(FPR, TPR)
        plt.plot([0, 1], [0, 1])
        plt.savefig(config.figure_save_path + "{}predict_{}_with_{}_pseudoROC.png".format(config.continue_flag, label_name[i], config.picturename))


def main(config):
    logger = load_logger(config)
    try:
        np.random.seed(config.random_seed)  # 设置随机种子，保证可复现
        data_gainer = Data(config)

        # 训练模型的模式
        if config.do_train:
            train_X, valid_X, train_Y, valid_Y = data_gainer.get_train_and_valid_data()
            train(config, logger, [train_X, train_Y, valid_X, valid_Y])
            test_X, test_Y = data_gainer.get_test_data(return_label_data=True)
            pred_result = predict(config, test_X)       # 这里输出的是未还原的归一化预测数据
            draw(config, data_gainer, logger, pred_result)
            ROC(config, data_gainer, pred_result)

        # 使用模型预测的模式
        if not config.do_train:
            test_X, test_Y = data_gainer.get_test_data(return_label_data=True)
            pred_result = predict(config, test_X)       # 这里输出的是未还原的归一化预测数据
            draw(config, data_gainer, logger, pred_result)
            
    except Exception:
        logger.error("Run Error", exc_info=True)

if __name__=="__main__":
    comm_type = '钢材'
    time_s = 20
    predict_d = 5
    total_cols = 22
    model_name = 'model_lstm.pth'
    lstm_layer = 2
    dropout_rate = 0.5
    batch_size = 500
    learning_rate = 0.001
    hidden_size = 150
    epoch = 1000
    patience = 10
    do_train = True
    train_data = 'steel.xlsx'
    predict_data = 'steel_predict.xlsx'
    con = Config(comm_type, int(time_s), int(predict_d), int(total_cols), model_name, int(lstm_layer), float(dropout_rate), int(batch_size), float(learning_rate), int(hidden_size), int(epoch), int(patience), do_train, train_data, predict_data)

    main(con)