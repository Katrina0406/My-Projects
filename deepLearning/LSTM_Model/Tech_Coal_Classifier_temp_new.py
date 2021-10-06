import pandas as pd
import numpy as np
import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from LSTM_model import train, predict

frame = "pytorch"

class Config:

    # 数据参数
    feature_columns = list(range(16))     # 要作为feature的列，按原数据从0开始计算，也可以用list 如 [2,4,6,8] 设置
    label_columns = [15]                  # 要预测的列，按原数据从0开始计算, 如同时预测第3，4,5列 1日收益率、5日收益率、10日收益率的label
    label_in_feature_index = (lambda x,y: [x.index(i) for i in y])(feature_columns, label_columns)  # 因为feature不一定从0开始


    # 网络参数
    input_size = len(feature_columns)
    output_size = len(label_columns)

    hidden_size = 32            # LSTM的隐藏层大小，也是输出大小
    lstm_layers = 2            # LSTM的堆叠层数
    dropout_rate = 0.2          # dropout概率
    time_step = 30              # 这个参数很重要，是设置用前多少天的数据来预测，也是LSTM的time step数
    predict_day = 5             # 预测未来几天

    picturename = '(Tech_Coal_Classifier_temp)'

    # 训练参数
    do_train = True
    do_predict = True
    add_train = False           # 是否载入已有模型参数进行增量训练
    shuffle_train_data = True   # 是否对训练数据做shuffle
    use_cuda = False            # 是否使用GPU训练

    train_data_rate = 0.9      # 训练数据占总体数据比例，测试数据就是 1-train_data_rate
    valid_data_rate = 0.1      # 验证数据占训练数据比例，验证集在训练过程使用，为了做模型和参数选择

    batch_size = 64
    learning_rate = 0.001
    epoch = 50                 # 整个训练集被训练多少遍，不考虑早停的前提下
    patience = 5                # 训练多少epoch，验证集没提升就停掉
    random_seed = 42            # 随机种子，保证可复现

    do_continue_train = False    # 每次训练把上一次的final_state作为下一次的init_state
    continue_flag = ""           # 但实际效果不佳，可能原因：仅能以 batch_size = 1 训练
    if do_continue_train:
        shuffle_train_data = False
        batch_size = 1
        continue_flag = "continue_"

    # 训练模式
    debug_mode = False  # 调试模式下，是为了跑通代码，追求快
    debug_num = 500  # 仅用debug_num条数据来调试

    # 框架参数
    used_frame = frame
    model_postfix = {"pytorch": ".pth"}
    model_name = "model_" + continue_flag + used_frame + model_postfix[used_frame]

    # 路径参数
    train_data_path = r"iron_ore.xlsx"
    model_save_path = r"DeepLearning/" + model_name + "/"
    figure_save_path = r"DeepLearning/"
    log_save_path = r"DeepLearning/"
    do_log_print_to_screen = True
    do_log_save_to_file = True
    do_figure_save = True
    do_train_visualized = False

    if not os.path.exists(model_save_path):
        os.makedirs(model_save_path)
    if not os.path.exists(figure_save_path):
        os.mkdir(figure_save_path)
    if do_train and (do_log_save_to_file or do_train_visualized):
        cur_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        log_save_path = log_save_path + cur_time + '_' + used_frame + "/"
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

    def read_data(self):                # 读取初始数据
        if self.config.debug_mode:
            init_data = pd.read_excel(self.config.train_data_path, nrows=self.config.debug_num, usecols=self.config.feature_columns)
            init_data = to_num(init_data)
            init_data.interpolate(method='values', inplace=True)
            init_data.fillna(method='ffill', inplace=True)
            init_data.fillna(method='bfill', inplace=True)
            print(init_data.isnull().any())
        else:
            init_data = pd.read_excel(self.config.train_data_path, usecols=self.config.feature_columns)
            init_data = to_num(init_data)
            init_data.interpolate(method='values', inplace=True)
            init_data.fillna(method='ffill', inplace=True)
            init_data.fillna(method='bfill', inplace=True)
            print(init_data.isnull().any())
        return init_data.values, init_data.columns.tolist()     # .columns.tolist() 是获取列名

    def get_train_and_valid_data(self):
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

    def get_test_data(self, return_label_data=False):
        feature_data = self.norm_data[self.train_num:]
        self.start_num_in_test = feature_data.shape[0] % self.config.time_step  # 这些天的数据不够一个time_step
        time_step_size = feature_data.shape[0] // self.config.time_step

        # 在测试数据中，每time_step行数据会作为一个样本，两个样本错开time_step行
        # 比如：1-20行，21-40行。。。到数据末尾。
        test_x = [feature_data[self.start_num_in_test+i*self.config.time_step : self.start_num_in_test+(i+1)*self.config.time_step]
                   for i in range(time_step_size)]
        if return_label_data:       # 实际应用中的测试集是没有label数据的
            label_data = self.norm_data[self.train_num + self.start_num_in_test:, self.config.label_in_feature_index]
            return np.array(test_x), label_data
        return np.array(test_x)

# 将dataframe里面所有列的类型都转化为float，方便后续进行模型训练
def to_num(df):

    cols = df.columns
    for col in cols:
        if not isinstance(df[col].dtype, float):
            df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    
    return df

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

def draw(config: Config, origin_data: Data, logger, predict_norm_data: np.ndarray):
    label_data = origin_data.data[origin_data.train_num + origin_data.start_num_in_test : ,
                                            config.label_in_feature_index]
    predict_data = predict_norm_data * origin_data.std[config.label_in_feature_index] + \
                   origin_data.mean[config.label_in_feature_index]   # 通过保存的均值和方差还原数据
    assert label_data.shape[0]==predict_data.shape[0], "The element number in origin and predicted data is different"

    label_name = [origin_data.data_column_name[i] for i in config.label_in_feature_index]
    label_column_num = len(config.label_columns)

    loss = np.mean((label_data[config.predict_day:] - predict_data[:-config.predict_day] ) ** 2, axis=0)
    loss_norm = loss/(origin_data.std[config.label_in_feature_index] ** 2)
    logger.info("The mean squared error of stock {} is ".format(label_name) + str(loss_norm))

    label_X = range(origin_data.data_num - origin_data.train_num - origin_data.start_num_in_test)
    predict_X = [ x + config.predict_day for x in label_X]

    for i in range(label_column_num):
        Retthresholdup   =  0.02
        Retthresholddown =  -0.02
        predict_data[:, i][predict_data[:, i] >  Retthresholdup ] = 2
        predict_data[:, i][(predict_data[:, i] < Retthresholddown ) & (predict_data[:, i] > Retthresholdup)] = 1
        predict_data[:, i][predict_data[:, i] < Retthresholddown] = 0

        plt.figure(i+1)                     # 预测数据绘制
        plt.plot(label_X, label_data[:, i], label='label')
        plt.plot(predict_X, predict_data[:, i], label='predict')

        plt.title("LSTM {} testing performance on  {}".format(config.picturename,label_name[i]))
        logger.info("The predicted Rebar {} for the next {} day(s) is: ".format(label_name[i], config.predict_day) +
                str(np.squeeze(predict_data[-config.predict_day:, i])))
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
        print('严趋势判准率:{:.2f}%'.format(100 * np.trace(resMatrix) / point_prediction.shape[0]))
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
        plt.savefig(config.figure_save_path + "{}predict_{}_with_{}_pseudoROC.png".format(config.continue_flag, label_name[i],config.picturename))


def main(config):
    logger = load_logger(config)
    try:
        np.random.seed(config.random_seed)  # 设置随机种子，保证可复现
        data_gainer = Data(config)

        if config.do_train:
            train_X, valid_X, train_Y, valid_Y = data_gainer.get_train_and_valid_data()
            train(config, logger, [train_X, train_Y, valid_X, valid_Y])

        if config.do_predict:
            test_X, test_Y = data_gainer.get_test_data(return_label_data=True)
            pred_result = predict(config, test_X)       # 这里输出的是未还原的归一化预测数据
            draw(config, data_gainer, logger, pred_result)
            ROC(config, data_gainer, pred_result)
    except Exception:
        logger.error("Run Error", exc_info=True)


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    con = Config()
    for key in dir(args):
        if not key.startswith("_"):
            setattr(con, key, getattr(args, key))

    main(con)