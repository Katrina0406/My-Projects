from django.shortcuts import render, HttpResponse
import xlrd
from rfapp.class_model import RFModel

# Create your views here.
def get_info_rf(request):

    if request.method == 'POST':

        comm_type = request.POST.get('type')
        time_step = request.POST.get('time_step')
        predict_step = request.POST.get('predict_step')
        model_name = request.POST.get('model_name')
        excel_file = request.POST.get('excel_file')

        criterion = request.POST.get('criterion')
        max_depth = request.POST.get('max_depth')
        n_estimators = request.POST.get('n_estimators')
        max_features = request.POST.get('max_features')
        min_samples_split = request.POST.get('min_samples_split')
        random_state = request.POST.get('random_state')
        min_samples_leaf = request.POST.get('min_samples_leaf')

        if criterion != '':
            # 训练模式

            criterion = criterion.split(",")
            max_depth = max_depth.split(",")
            n_estimators = n_estimators.split(",")
            max_features = max_features.split(",")
            min_samples_split = min_samples_split.split(",")
            random_state = random_state.split(",")
            min_samples_leaf = min_samples_leaf.split(",")

            param_grid = {
                    'criterion':criterion,
                    'max_depth':range(int(max_depth[0]), int(max_depth[1]), int(max_depth[2])),    # 深度：这里是森林中每棵决策树的深度，如果想自动生成深度的话用None
                    'n_estimators':range(int(n_estimators[0]), int(n_estimators[1]), int(n_estimators[2])),  # 决策树个数-随机森林特有参数
                    # 暂时把max_features定义成这三种，可以修改
                    'max_features':['auto', 'log2', 'sqrt'], # 每棵决策树使用的变量占比-随机森林特有参数（结合原理）
                    'min_samples_split':range(int(min_samples_split[0]), int(min_samples_split[1]), int(min_samples_split[2])),  # 叶子的最小拆分样本量
                    'random_state': range(int(random_state[0]), int(random_state[1]), int(random_state[2])),
                    'class_weight': [None, 'balanced'],
                    'min_samples_leaf': range(int(min_samples_leaf[0]), int(min_samples_leaf[1]), int(min_samples_leaf[2]))
                }

            # 创建一个随机森林project
            RF = RFModel(comm_type, int(time_step), int(predict_step), excel_file, param_grid, model_name)

             # 训练一个随机森林模型
            RF.run_train_process()

            # 评估模型性能（预测的时候不用）
            RF.run_evaluate_process()

            # 将训练完的模型保存到当前文件夹内
            RF.save_model()

        else:
            # 预测模式

            RF = RFModel(comm_type, int(time_step), int(predict_step), None, None, model_name, excel_file)

            RF.run_predict_process()


    return render(request, "rf.html")

