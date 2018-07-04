# -*- coding: utf-8 -*
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import misc


SAMPLE_NUM = 10
CLASS_NUM = 40
IMG_SHAPE = (112, 92)

scale = 0.5
k = 8
principal_percent = 0.8


def load_faceimg(path_dir, shrink_rate=0.5, train_rate=0.8):

    sample_k = int(train_rate * SAMPLE_NUM)
    train_m = int(train_rate * SAMPLE_NUM * CLASS_NUM)
    test_m = int((1 - train_rate) * SAMPLE_NUM * CLASS_NUM) + 1
    shape0 = int(IMG_SHAPE[0] * shrink_rate)
    shape1 = int(IMG_SHAPE[1] * shrink_rate)

    train_x = np.zeros((train_m, shape0 * shape1))
    train_y = np.zeros(train_m).astype(np.int8)
    test_x = np.zeros((test_m, shape0 * shape1))
    test_y = np.zeros(test_m).astype(np.int8)
    print train_x.shape, test_x.shape

    for i in range(CLASS_NUM):
            face_lable = i + 1
            for j in range(SAMPLE_NUM):
                filename = path_dir + '/s' + str(face_lable) + '/' + str(j + 1) + '.pgm'
                img = misc.imresize(mpimg.imread(filename), shrink_rate).flatten().astype(np.float)
                if j < sample_k:
                    train_x[i * sample_k + j, :] = img
                    train_y[i * sample_k + j] = face_lable
                if j >= sample_k:
                    test_x[i * (10 - sample_k) + (j - sample_k), :] = img
                    test_y[i * (10 - sample_k) + (j - sample_k)] = face_lable

    return train_x, train_y, test_x, test_y


# 0均值化
def zero_mean(train_x, test_x):
    mean_x = train_x.mean(axis = 0).reshape(1, train_x.shape[1])
    train_x = train_x - np.repeat(mean_x, train_x.shape[0], axis = 0)
    test_x = test_x - np.repeat(mean_x, test_x.shape[0], axis=0)
    return train_x, test_x


# PCA降维
def pca(train_x, test_x, threshold):
    # step1.零均值化
    train_x, test_x = zero_mean(train_x, test_x)

    # step2.协方差矩阵
    cov = np.cov(train_x, rowvar=0)

    # step3.求特征值、特征向量并排序，以及贡献率对应的n值
    eig_vals, eig_vecs = np.linalg.eig(cov)
    n = threshold_trans(eig_vals, threshold)
    eig = np.vstack((eig_vals, eig_vecs))
    eig_vecs = np.delete(eig.T[np.lexsort(eig[::-1, :])].T[:, ::-1], 0, axis=0)

    # step4.选择前n个特征向量作为基，降维
    # n = int(eig_vecs.shape[1]*principal_percent)
    eig_vecs = eig_vecs[:, 0:n]
    train_x = np.dot(train_x, eig_vecs)
    test_x = np.dot(test_x, eig_vecs)

    return train_x, test_x, eig_vecs


def threshold_trans(values, ths):
    all_values = sum(values)
    sorted_values = np.sort(values)
    sorted_values = sorted_values[-1::-1]
    part_values = 0
    n = 0
    for value in sorted_values:
        part_values += value
        n += 1
        if part_values >= all_values * ths:
            return n


def predict(train_x, train_y, test_x, test_y):
    # recognise via measuring educlidean distance in high dimentional space
    count = 0
    for i in range(test_x.shape[0]):
        test_x1 = test_x[i, :].reshape((1, test_x.shape[1]))
        sub = train_x - np.repeat(test_x1, train_x.shape[0], axis=0)
        dis = np.linalg.norm(sub, axis=1)
        fig = np.argmin(dis)
        # print i, train_y[fig], test_y[i]
        if train_y[fig] == test_y[i]:
            count += 1

    return count


def plot_face(img):
    plt.figure('low dimension map')
    r, c = (4, 10)
    for i in range(r * c):
        plt.subplot(r, c, i + 1)
        x = int(math.sqrt(img.shape[1]))
        plt.imshow(img[:, i].real.reshape(int(112*0.5), int(92*0.5)), cmap='gray')
        plt.axis('off')
    plt.show()


threshold = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.999, 0.999999]
# 载入数据集
print '[INFO]loading...'
train_xs, train_y, test_xs, test_y = load_faceimg(os.getcwd() + '/data')
# pca降维
print '[INFO]PCA...'
for ths in threshold:
    train_x, test_x, eig_vecs = pca(train_xs, test_xs, ths)
    print ths, train_x.shape
    # 预测
    count = predict(train_x, train_y, test_x, test_y)
    correct_rate = count * 1.0 / test_x.shape[0]
    print "Correct rate =", correct_rate * 100, "%"
    if train_x.shape[1] > 40:
        plot_face(eig_vecs)