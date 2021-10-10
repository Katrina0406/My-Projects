# Random Forest model
——Applicable scenarios: small and medium data volume

## idea:
It is composed of many decision trees, and different decision trees are not related. result. Which of the classification results of the decision tree has the most classification, the probability of occurrence will appear this result.

#### Accuracy: 
accuracy = number of days predicted increase while is actually increase / all days predicted increase
#### Recall
recall = number of days predicted increase while is actually increase / all days actually increase
#### F1-score
f1-score: measure the rationality of the two-class model, balance rate and numerical rate
= 2 * precision * recall rate / (precision + recall rate)
#### Support
Support: the number of days of possible changes/cancellations in the original sample

### Classification effect:
1. The greater the correlation between any two trees in the forest, the greater the error rate
2. The stronger the classification ability of each tree in the forest, the lower the error rate of the entire forest

### advantage:
    1. High-dimensional data (multiple features) can be produced without dimensionality reduction or feature selection
    2. The importance of features can be judged
    3. Can judge the mutual influence between different characteristics
    4. Not easy to overfit
    5. The training speed is relatively fast, and it is easy to make a parallel method
    6. Simple to implement
    7. For unbalanced data sets, errors can be balanced
    8. If a large part of the features are missing, the accuracy can still be maintained

### shortcoming:
    1. Overfitting on some noisy classification or regression problems
    2. For data with attributes with different values, attributes with more value divisions will have a greater impact on the random forest, 
       so the attribute weights produced by the random forest on this kind of data are unreliable
       
### data processing:
    1. Delete indicators with too many missing values. Generally, the missing data in a column of data accounts for more than 20% of the total data and must be cleaned up, otherwise it will affect the accuracy of the model. 
    However, since many data are monthly, if you calculate by day, there will be only one day in a month, so you manually clean up such data columns. clean_columns is only applicable to clean up all data sets in days.
    2. Fill in missing values (the code has been written, the idea is to fill in with a linear function first to form a rough trend, and then use the data above/below it to fill in if there are missing values.
    3. Clean up indicators that are too relevant to improve the accuracy of the model (code has been written, and the clean_relation method can be implemented). 
    If the correlation between variables is too strong, the variables will be invalid/affect the training of the model, and it will also slow down the training process. Only one of the two variables with high correlation is selected and kept. 
    Generally, more than 80% of the variables must be cleaned up even if the correlation is very high.
    4. Train the random forest model (using the classifier directly or with the help of GridSearchCV).
    5. Adjust the parameters, the idea is to adjust each parameter independently (other parameters remain unchanged, 
    only one parameter range changes at a time, given a range for the computer to calculate the best parameter value).
    6. Overall thinking of parameters:
#### Frame parameters:
        (1) n_estimators (the largest number of weak learners):
    Generally speaking, if n_estimators is too small, it is easy to underfit. If n_estimators is too large, the amount of calculation will be too large, and after n_estimators reaches a certain number, 
    the model improvement obtained by increasing n_estimators will be small, so generally choose a moderate value. The default is 100.
        (2) oob_score (whether to use out-of-bag samples to evaluate the quality of the model):
    The default recognition is False. Personally recommend setting it to True, because the out-of-bag score reflects the generalization ability of a model after fitting.
        (3) Criterion (that is, the evaluation criteria for features when the CART tree is divided):
    The loss function of classification model and regression model is different. The CART classification tree corresponding to the classification RF defaults to the Gini coefficient gini, 
    and another optional criterion is the information gain. The CART regression tree corresponding to the regression RF defaults to the mean square error.
    
#### Decision tree parameters:
        (1) max_features (the maximum number of features considered during RF division):
    Many types of values ​​can be used. The default is "auto", which means that at most √𝑁 features will be considered when dividing; 
    if it is "log2", it means that at most 𝑙𝑜𝑔2𝑁 features will be considered when dividing; 
    if it is "sqrt" or "auto" it means When dividing, consider at most √𝑁 features. 
    If it is an integer, it represents the absolute number of features considered. 
    If it is a floating point number, it means that the percentage of features is considered, that is, 
    the number of features rounded up to (percent xN) is considered. Where N is the total number of features of the sample. 
    Generally, we can use the default "auto". If the number of features is very large, we can flexibly use the other values 
    just described to control the maximum number of features considered during division to control the generation time of the decision tree.
    
        (2) max_depth (the maximum depth of the decision tree):
    The default is not to enter, if you do not enter, the decision tree will not limit the depth of the subtree when it builds the subtree. 
    Generally speaking, this value can be ignored when there are few data or features. If the model has a large sample size and many features, 
    it is recommended to limit this maximum depth. The specific value depends on the distribution of the data. Commonly used values can be between 10-100.
    
        (3) min_samples_split (the minimum number of samples required for subdividing internal nodes):
     This value limits the conditions for the continued division of the subtree. If the number of samples of a node is less than min_samples_split, 
     it will not continue to try to select the optimal feature for division. The default is 2. 
     If the sample size is not large, you do not need to control this value. If the sample size is very large, it is recommended to increase this value.
     
        (4) min_samples_leaf (minimum number of samples of leaf nodes):
     This value limits the minimum number of samples of leaf nodes. If the number of a leaf node is less than the number of samples, it will be pruned together with its sibling nodes. 
     The default is 1, you can enter the integer of the minimum number of samples, or the minimum number of samples as a percentage of the total number of samples. 
     If the sample size is not large, you do not need to control this value. If the sample size is very large, it is recommended to increase this value.
     
        (5) min_weight_fraction_leaf (the smallest sample weight sum of leaf nodes):
    This value limits the minimum value of the weight sum of all samples of the leaf node. If it is less than this value, 
    it will be pruned together with the sibling nodes. The default is 0, that is, the weight issue is not considered. 
    Generally speaking, if we have more samples with missing values, or if the distribution category of the classification tree samples has a large deviation, 
    the sample weight will be introduced. At this time, we must pay attention to this value.
    
        (6) max_leaf_nodes (the maximum number of leaf nodes):
    By limiting the maximum number of leaf nodes, overfitting can be prevented. The default is "None", that is, the maximum number of leaf nodes is not limited. 
    If a restriction is added, the algorithm will build the optimal decision tree within the maximum number of leaf nodes. 
    If there are not many features, this value can be ignored, but if there are too many features, it can be restricted. 
    The specific value can be obtained through cross-validation.
    
        (7) min_impurity_split (minimum impurity of node division):
    This value limits the growth of the decision tree. If the impurity of a node (based on Gini coefficient, mean square error) is less than this threshold, 
    the node no longer generates child nodes. It is a leaf node. It is generally not recommended to change the default value 1e-7.
    
# Neural network LSTM model
——Applicable scenario: large data volume

## LSTM model introduction:
Long short-term memory (Long short-term memory, LSTM) is a special kind of RNN, mainly to solve the problem of gradient disappearance and gradient explosion during long sequence training. LSTM is very suitable for dealing with problems that are highly related to time series, such as machine translation, dialog generation, encoding\decoding, etc.

### LSTM_model file:
     (1) The custom LSTM module is responsible for training the model and predicting the data trend, which is called in Tech_Coal_Classifier_temp
     (2) The python package used: pytorch, which provides an LSTM model and helps transform the data into a trainable structure
    
### Tech_Coal_Classifier_temp file:
     (1) Assign values to the LSTM model in the Config class, and define various training parameters. The input data can be replaced by changing the path parameter.
     (2) Read and process the data in the Data class to obtain the trained data
     (3) The draw method can customize the graph of the training process
     (4) ROC method outputs prediction results

### The new data set needs to be changed:
     1. The read_data() function should be changed to pd.read_csv or pd_read_excel according to the input file.
     2. The parameters need to be modified, and the range of columns cannot exceed the original value of the data set
     3. Missing values need to be processed, nan is not supported, so there must be data in all positions (processed in Data)
     4. The triple_class_accuracy() function for judging the rise or fall also needs to be modified according to the data, and the ROC function also needs to be modified according to the content of the data
     To change, 012 in the original example represents fall, shock, and rise respectively, so the data conversion of 012 is performed to output the result.
    
### Parameter meaning:
1. Dropout: Most of the Dropout papers are set to 0.5. It is said that 0.5 works well and can prevent over-fitting problems. However, in different tasks, you need to adjust the size of the dropout appropriately, 
and adjust the value of the dropout. In addition, the position of dropout in the model is also very important. You can try different dropout positions, and you may get amazing results.

2. Batch size: The batch size still needs to be adjusted appropriately. See related blogs. Generally, the setting will not exceed 128, and it may be very small. 
In my current task, batch size = 16 has a good effect.

3. Learning rate: The general initial value of learning rate is different for different optimizer settings. It is said that there are some classic configurations, such as Adam: lr = 0.001

4. The number of epoch iterations: set different values ​​according to your task, model, convergence speed, and fitting effect

5. Hidden size: The dimensionality of the hidden layer in LSTM also has a certain impact on the result. If you use a 300dim external word vector, you can consider hidden size = 150 or 300. 
For the hidden size, I set the maximum to 600 because of the hardware Because of the equipment, 600 is already very slow to train. If the hardware resources are ok, you can try more hidden size values, 
but in the process of trying, you still have to consider the relationship between the hidden size and the word vector dimension (I think it is Have a certain relationship influence)

6. lstm layer The number of stacked layers: the more layers, the deeper the training layer. Simply stacking LSTM layers can work up to 4 layers, rarely work 6 layers, and it is very bad if more than 8 layers.
    
    
    
    
    
    
    
    
    
    
    
    