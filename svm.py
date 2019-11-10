import sys
import numpy as np
import segment
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.externals import joblib

seg = segment.segment()
print('(1) load texts...')

pos_train_filename = r'data\source\normal.txt'
neg_train_filename = r'data\source\die.txt'
pos_eval_filename = r'data\source\normal_test.txt'
neg_eval_filename = r'data\source\die_test.txt'

origin_pos_train = open(pos_train_filename, encoding='UTF-8').read().split('\n')
origin_neg_train = open(neg_train_filename, encoding='UTF-8').read().split('\n')
origin_pos_eval = open(pos_eval_filename, encoding='UTF-8').read().split('\n')
origin_neg_eval = open(neg_eval_filename, encoding='UTF-8').read().split('\n')

pos_train_dir, pos_train_label_dir = seg.seg_lines_list(1, pos_train_filename)
neg_train_dir, neg_train_label_dir = seg.seg_lines_list(0, neg_train_filename)
pos_test_dir, pos_test_label_dir = seg.seg_lines_list(1, pos_eval_filename)
neg_test_dir, neg_test_label_dir = seg.seg_lines_list(0, neg_eval_filename)

train_pos = open(pos_train_dir, encoding='UTF-8').read().split('\n')
train_neg = open(neg_train_dir, encoding='UTF-8').read().split('\n')
test_pos = open(pos_test_dir, encoding='UTF-8').read().split('\n')
test_neg = open(neg_test_dir, encoding='UTF-8').read().split('\n')

train_pos_label = open(pos_train_label_dir, encoding='UTF-8').read().split('\n')
train_neg_label = open(neg_train_label_dir, encoding='UTF-8').read().split('\n')
test_pos_label = open(pos_test_label_dir, encoding='UTF-8').read().split('\n')
test_neg_label = open(neg_test_label_dir, encoding='UTF-8').read().split('\n')

origin_train_text = origin_pos_train + origin_neg_train
origin_eval_text = origin_pos_eval + origin_neg_eval
train_texts = train_pos + train_neg
test_texts = test_pos + test_neg
train_labels = train_pos_label + train_neg_label
test_labels = test_pos_label + test_neg_label

all_text = train_texts + test_texts
all_labels = train_labels + test_labels

print('(2) doc to var...')
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# CountVectorizer考虑每种词汇在该训练文本中出现的频率，得到计数矩阵
count_v0= CountVectorizer(analyzer='word',token_pattern='\w{1,}')
counts_all = count_v0.fit_transform(all_text)

count_v1= CountVectorizer(vocabulary=count_v0.vocabulary_)
counts_train = count_v1.fit_transform(train_texts) 
print("the shape of train is "+repr(counts_train.shape)  )
count_v2 = CountVectorizer(vocabulary=count_v0.vocabulary_)
counts_test = count_v2.fit_transform(test_texts)
print("the shape of test is "+repr(counts_test.shape)  )

# 保存数字化后的词典
joblib.dump(count_v0.vocabulary_, "model/die_svm_20191110_vocab.m")

counts_all = count_v2.fit_transform(all_text)
print("the shape of all is "+repr(counts_all.shape))

# 将计数矩阵转换为规格化的tf-idf格式
tfidftransformer = TfidfTransformer()  
train_data = tfidftransformer.fit(counts_train).transform(counts_train)
test_data = tfidftransformer.fit(counts_test).transform(counts_test)
all_data = tfidftransformer.fit(counts_all).transform(counts_all)

train_data = counts_train
test_data = counts_test
all_data = counts_all

x_train = train_data
y_train = train_labels
x_test = test_data
y_test = test_labels

print('(3) SVM...')
from sklearn.svm import SVC

# 使用线性核函数的SVM分类器，并启用概率估计（分别显示分到两个类别的概率如：[0.12983359 0.87016641]）
svclf = SVC(kernel = 'linear', probability=True) 

# 开始训练
svclf.fit(x_train,y_train)
# 保存模型
joblib.dump(svclf, "model/die_svm_20191110.m")

# 测试集进行测试
preds = svclf.predict(x_test)
y_preds = svclf.predict_proba(x_test)

preds = preds.tolist()
for i,pred in enumerate(preds):
    # 显示被分错的微博
    if int(pred) != int(y_test[i]):
        try:
            print(origin_eval_text[i], ':', test_texts[i], pred, y_test[i], y_preds[i])
        except Exception as e:
            print(e)

# 分别查看两个类别的准确率、召回率和F1值
print(classification_report(y_test, preds))