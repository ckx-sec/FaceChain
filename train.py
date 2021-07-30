from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier  # K近邻分类器
from sklearn.tree import DecisionTreeClassifier  # 决策树分类器
from sklearn.naive_bayes import GaussianNB  # 高斯朴素贝叶斯函数
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import fetch_lfw_people
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV # 调节参数
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import random
import time
import csv

import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)

def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist


def loadData(path, num):
    data = []
    for i in range(num): # 修改
        csv_reader = csv.reader(open(path + "/modify" + str(i) + ".csv"))
        # for row in csv_reader:
        #     print(row)
        f = []
        for row in csv_reader:
            tmp = list(map(lambda x:float(x),row))
            for t in tmp:
                f.append(t)
        # print(len(f))
        data.append(f)
    # print(data)
    return data

def getXmean(x_train):
    return np.mean(x_train, axis=0)

def centralized(x_test, mean):
    x_test -= mean
    return x_test


# 归一化
x_train = loadData("./datasets/train/modify_13+20+6_e_10", 33)
mean = getXmean(x_train)
print(type(mean))
# x_train = centralized(x_train, mean)
x_test = loadData("./datasets/test/modify_13+20+6_e_10", 6)
# x_test = centralized(x_test, mean)

y_train = []
for i in range(33):
    y_train.append(i)

y_test = [0,1,2,3,4,6]

cc = list(zip(x_train, y_train))
random.shuffle(cc)
x_train[:], y_train[:] = zip(*cc)

cc = list(zip(x_test, y_test))
random.shuffle(cc)
x_test[:], y_test[:] = zip(*cc)


#########################
# 降维
# pca = PCA(n_components=30, # 主成分
#           svd_solver='randomized', # 随机打乱
#           whiten=True) # 白化
# # print(type(x_train))
# tmp = np.concatenate((x_train, x_test), axis=0)
# pca.fit(tmp)

# x_train = pca.transform(x_train) # 预处理x_train
# x_test = pca.transform(x_test)
# print(x_test)
#########################

# ########################
# # 计算欧氏距离
# result = []
# for i in x_test:
#     dis = []
#     for j in x_train:
#         dis.append(return_euclidean_distance(i, j))
#     result.append(dis)
#     # m = 999999999
#     # index = -1
#     # for d in range(len(dis)):
#     #     if dis[d] < m:
#     #         m = dis[d]
#     #         index = d
#     # result.append(index)
# for r in result:
#     print(r)
# ########################

svc_last = SVC(C=5.0, gamma=0.001, max_iter=-1)

start = time.time()
start = int(round(start * 1000))

svc_last.fit(x_train, y_train)

end = time.time()
end = int(round(end * 1000))

y_new = svc_last.predict(x_test)
print("svc:")
print(y_new)
print(end-start)
print(classification_report(y_test, y_new))

# knn适用于低维
# knn = KNeighborsClassifier().fit(x_train, y_train)
# answer_knn = knn.predict(x_test)
# print("knn:",answer_knn)
# print(classification_report(y_test, answer_knn))

start = time.time()
start = int(round(start * 1000))
gnb = GaussianNB().fit(x_train, y_train)
end = time.time()
end = int(round(end * 1000))

answer_gnb = gnb.predict(x_test)
print("gnb:", answer_gnb)
print(end-start)
print(classification_report(y_test, answer_gnb))

# 适用于低维
start = time.time()
start = int(round(start * 1000))
mlp = MLPClassifier().fit(x_train, y_train)
end = time.time()
end = int(round(end * 1000))

answer_mlp = mlp.predict(x_test)
print("mlp:", answer_mlp)
print(end-start)
print(classification_report(y_test, answer_mlp))
