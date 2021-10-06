#调参文档代码及说明

##整体调参：直接使用网格搜索
————替换参数的调整范围、可添加新的random forest模型参数
    param_grid = {
        'criterion':['entropy','gini'],
        'max_depth':range(5, 40, 5),    # 深度：这里是森林中每棵决策树的深度
        'n_estimators':range(50, 100, 2),  # 决策树个数-随机森林特有参数
        'max_features':[0.1, 0.2, 0.3, 0.6, 0.75, 0.95], # 每棵决策树使用的变量占比-随机森林特有参数（结合原理）
        'min_samples_split':[4,8,12,16,24,28]  # 叶子的最小拆分样本量
    }

##分步骤调参数 
————单独运行每一个param_test获取每个参数的最优值
    
###调参1: n_estimators
    param_test1 = {'n_estimators': range(270, 600, 10)}
    gsearch1 = GridSearchCV(estimator = RandomForestClassifier(min_samples_split=20, min_samples_leaf=5, max_depth=8, max_features=3, random_state=10), 
    param_grid=param_test1, scoring='roc_auc', cv=5)
    gsearch1.fit(x_train, y_train)
    print(gsearch1.best_params_, gsearch1.best_score_)

###调参2: min_samples_split
    param_test2 = {'min_samples_split': range(20, 400, 10)}
    gsearch2 = GridSearchCV(estimator = RandomForestClassifier(n_estimators=320, max_depth=8, max_features=10, min_samples_leaf = 50, random_state=10), 
    param_grid=param_test2, scoring='roc_auc', cv=5)
    gsearch2.fit(x_train, y_train)
    print(gsearch2.best_params_, gsearch2.best_score_)

###调参3: min_samples_leaf
    param_test3 = {'min_samples_leaf': range(10, 50, 5)}
    gsearch3 = GridSearchCV(estimator = RandomForestClassifier(n_estimators=320, max_depth=8, max_features=10, min_samples_split = 300, random_state=10), 
    param_grid=param_test3, scoring='roc_auc', cv=5)
    gsearch3.fit(x_train, y_train)
    print(gsearch3.best_params_, gsearch3.best_score_)

###调参4: max_depth
    param_test4 = {'max_depth': range(2, 20, 1)}
    gsearch4 = GridSearchCV(estimator = RandomForestClassifier(n_estimators=320, min_samples_split=300, min_samples_leaf=10, max_features=10, random_state=10), 
    param_grid=param_test4, scoring='roc_auc', cv=5)
    gsearch4.fit(x_train, y_train)
    print(gsearch4.best_params_, gsearch4.best_score_)

###调参5:  criterion & class_weight
    param_test5 = {'criterion': ['gini', 'entropy'], 'class_weight': [None, 'balanced']}
    gsearch5 = GridSearchCV(estimator = RandomForestClassifier(n_estimators=320, min_samples_split=300, min_samples_leaf=10, max_depth=14, max_features=10, random_state=10), param_grid=param_test5, scoring='roc_auc', cv=5)
    gsearch5.fit(x_train, y_train)
    print(gsearch5.best_params_, gsearch5.best_score_)

###调参6:  max_features
    param_test6 = {'max_features': range(1, 12, 1)}
    gsearch6= GridSearchCV(estimator = RandomForestClassifier(criterion='entropy', class_weight='balanced', n_estimators=320, min_samples_split=300, min_samples_leaf=10, max_depth=14, random_state=10), 
    param_grid=param_test6, scoring='roc_auc', cv=5)
    gsearch6.fit(x_train, y_train)
    print(gsearch6.best_params_, gsearch6.best_score_)

###调参7:  random_state
    param_test7 = {'random_state': range(1, 15, 1)}
    gsearch7 = GridSearchCV(estimator = RandomForestClassifier(criterion='entropy', class_weight='balanced', n_estimators=320, min_samples_split=300, min_samples_leaf=10, max_depth=14, max_features=11), 
    param_grid=param_test7, scoring='roc_auc', cv=5)
    gsearch7.fit(x_train, y_train)
    print(gsearch7.best_params_, gsearch7.best_score_)

##另一种调参方式：
————分数用的是cross validation会偏低

    score_lt = []

    for i in range(10):
        param_grid = {'max_features': [i]}
        gtest1 = GridSearchCV(estimator = RandomForestClassifier(n_estimators=370, min_samples_split=280, min_samples_leaf=90, random_state=10), scoring='roc_auc', param_grid=param_grid, cv=5)
        gtest1.fit(x_train, y_train)
        score = cross_val_score(gtest1, x_train, y_train, cv=10).mean()
        score_lt.append(score)
        score_max = max(score_lt)
    print('最大得分：{}'.format(score_max),
        '子树数量为：{}'.format(score_lt.index(score_max)))