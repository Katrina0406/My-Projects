from django.shortcuts import render, HttpResponse
from rfapp.lstm_run import Config, main
import argparse


# Create your views here.
def get_info_lstm(request):

    if request.method == 'POST':

        # time_s = 30
        # predict_d = 5
        # feature_col = list(range(1, 22)) 
        # label_col = [21]
        # train_data = 'steel.xlsx'
        # lstm_layers = 2            # LSTM的堆叠层数
        # dropout_rate = 0.2 
        # batch_size = 64
        # learning_rate = 0.001
        # hidden_size = 32
        # epoch = 50                 # 整个训练集被训练多少遍，不考虑早停的前提下
        # patience = 5

        comm_type = request.POST.get('comm_type')
        time_s = request.POST.get('time_s')
        predict_d = request.POST.get('predict_d')
        total_cols = request.POST.get('total_cols')
        model_name = request.POST.get('model_name')
        lstm_layer = request.POST.get('lstm_layer')
        dropout_rate = request.POST.get('dropout_rate')
        batch_size = request.POST.get('batch_size')
        learning_rate = request.POST.get('learning_rate')
        hidden_size = request.POST.get('hidden_size')
        epoch = request.POST.get('epoch')
        patience = request.POST.get('patience')
        do_train = request.POST.get('do_train')
        train_data = request.POST.get('train_data')
        predict_data = request.POST.get('predict_data')

        if do_train == 'True':
            do_train = True
        else:
            do_train = False

        con = Config(comm_type, int(time_s), int(predict_d), int(total_cols), model_name, int(lstm_layer), float(dropout_rate), int(batch_size), float(learning_rate), int(hidden_size), int(epoch), int(patience), do_train, train_data, predict_data)

        main(con)

    return render(request, "lstm.html")



