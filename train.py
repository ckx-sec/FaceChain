from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier  # K近邻分类器
from sklearn.tree import DecisionTreeClassifier  # 决策树分类器
from sklearn.naive_bayes import GaussianNB  # 高斯朴素贝叶斯函数
from sklearn.neural_network import MLPClassifier
import numpy as np

from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV # 调节参数
import random
import time
import csv

import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)


# 平均值
def getXmean(x_train:list):
    return np.mean(x_train, axis=0)

# 归一化
def centralized(x_test:list, mean:list):
    x_test -= mean
    return x_test

def preData(x_train:list, y_train:list, x_test:list, y_test:list):

    if len(x_train) != len(y_train) or len(x_test) != len(y_test):
        return

    if len(x_train) == 0 or len(x_test) == 0:
        return

    # 归一化
    # 暂时不需要，以后看情况
    # mean = getXmean(x_train)
    # x_train = centralized(x_train, mean)
    # x_test = centralized(x_test, mean)

    cc = list(zip(x_train, y_train))
    random.shuffle(cc)
    x_train[:], y_train[:] = zip(*cc)

    cc = list(zip(x_test, y_test))
    random.shuffle(cc)
    x_test[:], y_test[:] = zip(*cc)

    # 降维
    if len(x_train + y_train) < 150:
        n = len(x_train + y_train)
    else:
        n = 150
        
    pca = PCA(n_components=n, # 主成分
              svd_solver='randomized', # 随机打乱
              whiten=True) # 白化
    # print(type(x_train))
    tmp = np.concatenate((x_train, x_test), axis=0)
    pca.fit(tmp)

    x_train = pca.transform(x_train)
    x_test = pca.transform(x_test)
    
    return x_train, y_train, x_test, y_test

# 准确率
def accuracy(y_true:list, y_pred:list):
    if len(y_true) != len(y_pred):
        return
    num = 0
    for i in range(len(y_pred)):
        if y_pred[i] == y_true[i]:
            num += 1
    return num/len(y_pred)


# 如果每个节点都用一种模型，则每个节点训练的效果都会基本相同，
# 所以给出几种不同的模型
# 返回模型、准确率和训练时间
# 准确率相同的情况下，训练时间越少效果越好

def svcTrain(x_train:list, y_train:list, x_test:list, y_test:list):
    x_train, y_train, x_test, y_test = preData(x_train, y_train, x_test, y_test)

    start = time.time()
    start = int(round(start * 1000))

    svc_last = SVC(C=5.0, gamma=0.001, max_iter=-1)
    svc = svc_last.fit(x_train, y_train)

    end = time.time()
    end = int(round(end * 1000))

    answer_svc = svc_last.predict(x_test)
    return svc, accuracy(y_test, answer_svc), end-start


def gnbTrain(x_train:list, y_train:list, x_test:list, y_test:list):
    x_train, y_train, x_test, y_test = preData(x_train, y_train, x_test, y_test)
    
    start = time.time()
    start = int(round(start * 1000))

    gnb = GaussianNB().fit(x_train, y_train)

    end = time.time()
    end = int(round(end * 1000))

    answer_gnb = gnb.predict(x_test)
    return gnb, accuracy(y_test, answer_gnb), end-start


def mlpTrain(x_train:list, y_train:list, x_test:list, y_test:list):
    # 适用于低维
    x_train, y_train, x_test, y_test = preData(x_train, y_train, x_test, y_test)
    
    start = time.time()
    start = int(round(start * 1000))

    mlp = MLPClassifier().fit(x_train, y_train)
    
    end = time.time()
    end = int(round(end * 1000))

    answer_mlp = mlp.predict(x_test)
    return mlp, accuracy(y_test, answer_mlp), end-start
