# -*- coding: utf-8 -*-

from numpy import linalg
from nltk.stem.snowball import EnglishStemmer
import numpy as np
from random import shuffle
from scipy.spatial.distance import pdist, squareform
import cvxopt
import operator
import re
import tarfile
import base64

spam_file = "data/20021010_spam.tar.bz2"
easy_ham_file = "data/20021010_easy_ham.tar.bz2"


# 读取压缩的邮件文件
def read_email(filename, max_num = -1):
    emails = []
    num = 0
    with tarfile.open(filename, 'r:bz2') as f:
        for info in f:
            if not info.isfile():
                continue
            email = f.extractfile(info).read()
            emails.append(email)
            num += 1
            if max_num <= num and max_num != -1:
                break
    return emails


# 载入邮件数据
def load_data(num = -1):
    spam_data = read_email(spam_file, num)
    ham_data = read_email(easy_ham_file, num)
    return spam_data, ham_data


# 中文，韩文，base64处理
def mail_filter(mails):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    k = 0
    for mail in mails:
        if 'Encoding: base64' in mail:

            ss = mail.partition('\n\n')[-1].split('\n\n')
            l = [len(s) if ':' not in s and '>' not in s else 0 for s in ss]
            base64_s = ss[l.index(max(l))]

            try:
                mail.replace(base64_s, base64.decodestring(base64_s))
            except:
                mails.remove(mail)
        else:
            mail1 = mail.decode('utf-8', 'ignore')
            match = zhPattern.search(mail1)
            if match:
               mails.remove(mail)

    return mails


# 邮件预处理：去除邮件头部，统一小写，去词根
def preprocessing(email):
    regexes = {
        'email': re.compile(r'<?[^@\s]+?@[^@\s]+?\.[^@\s]+>?'),
        'html': re.compile(r'<[^<]*?>'),
        'url': re.compile(r'(http|https)://[^\s]*'),
        'number': re.compile(r'\d+'),
        'dollar': re.compile(r'\$+'),
        'clean': re.compile(r'[^\w\s]+'),
        'space': re.compile(r'[\s]+'),
    }
    replacements = {
        'email': ' emailaddr ',
        'html': ' ',
        'url': ' httpaddr ',
        'number': ' number ',
        'dollar': ' dollar '
    }
    stemmer = EnglishStemmer()

    # 1.strip_header
    email = email.partition('\n\n')[-1]
    # 2.lower
    email = email.lower()
    # 3.normalize
    for word in replacements:
        while re.search(regexes[word], email):
            email = re.sub(regexes[word], replacements[word], email)
    # 4.clean
    email = re.sub(regexes['clean'], ' ', email)
    email = re.sub(regexes['space'], ' ', email)
    # 5.to list
    words = email.split(' ')
    # stem
    email = [stemmer.stem(word) for word in words if word]

    return email


# 词频统计，返回出现次数大于设定阈值的词用于建立词向量
def count_words(words, deduplicate=True, threshold=100, maximum=0):
    counts = {}
    top_words = []
    for wl in words:
        if deduplicate:
            wl = set(wl)
        for word in wl:
            counts[word] = counts.get(word, 0) + 1

    counts = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
    for word, count in counts:
        if count > threshold and (not maximum or len(top_words) < maximum):
            top_words.append(word)

    return top_words


# 文档向量化
def featurize(word_list, feature_dict):

    v = np.zeros(len(feature_dict))
    for w in word_list:
        if w in feature_dict:
            v[feature_dict[w]] += 1
    return v


# 统计词频，建立TDM矩阵
def email_tdm(spams, hams):
    # 统计词频
    spams_words = count_words(spams)
    hams_words = count_words(hams)
    # 综合spam和ham 建立词汇表
    feature_vol = dict((w, i) for i, w in enumerate(set(spams_words).symmetric_difference(hams_words)))

    spams_v = [featurize(x, feature_vol) for x in spams]
    hams_v = [featurize(x, feature_vol) for x in hams]

    return spams_v, hams_v


# 建立numpy向量
def build_np(data1, data2):
    m = len(data1) + len(data2)
    n = len(data1[0])
    arr = np.zeros((m, n))
    for i, v in enumerate(data1 + data2):
        arr[i, :] = v
    y = np.hstack((np.ones(len(data1)), np.zeros(len(data2))))
    return arr, y


# shuffle，划分训练集，测试集
def data_split_5fold(spam_data, ham_data, train_rate=0.8):

    spam_num = len(spam_data)
    ham_num = len(ham_data)
    spam_index = range(spam_num)
    ham_index = range(ham_num)
    shuffle(spam_index)
    shuffle(ham_index)
    x_train_5fold, y_train_5fold, x_test_5fold, y_test_5fold = [], [], [], []

    for f in range(5):
        spam_train, ham_train, spam_test, ham_test = [], [], [], []
        for i in range(spam_num):
            if (i >= spam_num * (1 - train_rate) * f) and (i <= spam_num * (1 - train_rate) * (f + 1)):
                spam_test.append(spam_data[spam_index[i]])
            else:
                spam_train.append(spam_data[spam_index[i]])

        for i in range(ham_num):
            if (i >= ham_num * (1 - train_rate) * f) and (i <= ham_num * (1 - train_rate) * (f + 1)):
                ham_test.append(ham_data[ham_index[i]])
            else:
                ham_train.append(ham_data[ham_index[i]])

        d1, d2 = build_np(spam_train, ham_train)
        d3, d4 = build_np(spam_test, ham_test)
        x_train_5fold.append(d1)
        y_train_5fold.append(d2)
        x_test_5fold.append(d3)
        y_test_5fold.append(d4)

    return x_train_5fold, y_train_5fold, x_test_5fold, y_test_5fold


# 朴素贝叶斯分类器
def nBayesClassifier(traindata, trainlabel, testdata, testlabel, threshold):
    lambda_ = 0.01
    m = traindata.shape[1]

    # print '[INFO]naive bayes training...'
    n_y1 = sum(trainlabel)
    n_y0 = len(trainlabel) - sum(trainlabel)
    p_y1 = (n_y1 + lambda_) / (n_y0 + n_y1 + 2 * lambda_)
    p_y0 = 1 - p_y1

    traindata_y1 = (traindata[trainlabel == 1, :] > 0).astype(int)
    traindata_y0 = (traindata[trainlabel == 0, :] > 0).astype(int)

    p_xi_y1 = (sum(traindata_y1) + lambda_) / (n_y1 + 2 * lambda_)
    p_xi_y0 = (sum(traindata_y0) + lambda_) / (n_y0 + 2 * lambda_)

    # print '[INFO]naive bayes testing...'
    testdata = (testdata > 0).astype(int)

    test_p_y1 = testdata * p_xi_y1
    test_p_y0 = testdata * p_xi_y0
    test_p_y1[test_p_y1 == 0] = 1
    test_p_y0[test_p_y0 == 0] = 1
    test_p_y1 = test_p_y1.cumprod(axis=1)[:, -1] * p_y1
    test_p_y0 = test_p_y0.cumprod(axis=1)[:, -1] * p_y0

    y_predict = ((test_p_y1 / (test_p_y1 + test_p_y0)) > threshold).astype(int)
    y_test = testlabel.astype(int)
    sp = 1.0 * sum(y_predict & y_test) / sum(y_predict)
    sr = 1.0 * sum(y_predict & y_test) / sum(y_test)
    f = (sr * sp * 2) / (sp + sr)
    # print sp, sr, f
    return f


# 最小二乘分类器
def lsClassifier(traindata, trainlabel, testdata, testlabel, lambd):

    m, n = traindata.shape
    traindata = np.hstack((np.ones(m).reshape(m, 1), traindata))
    temp = np.dot(traindata.T, traindata) + lambd * np.eye(n + 1)
    w = np.dot(np.dot(np.linalg.inv(temp), traindata.T), trainlabel)

    m, n = testdata.shape
    testdata = np.hstack((np.ones(m).reshape(m, 1), testdata))
    y_predict = np.dot(testdata, w) >= 0.5
    accuracy = 1.0 * sum(y_predict == testlabel) / m
    # print accuracy

    y_predict = y_predict.astype(int)
    y_test = testlabel.astype(int)
    sp = 1.0 * sum(y_predict & y_test) / sum(y_predict)
    sr = 1.0 * sum(y_predict & y_test) / sum(y_test)
    f = (sr * sp * 2) / (sp + sr)
    # print sp, sr, f
    return f


def rbf_kernel(x, y, sigma=5.0):
    return np.exp(-linalg.norm(x - y) ** 2 / ((sigma ** 2)))


# 软边界支持向量机
def softsvm(traindata, trainlabel, testdata, testlabel, sigma=0.0, C=1.0):

    y = trainlabel * 2 - 1
    X = traindata
    n_samples, n_features = X.shape

    print X.shape, sigma, C
    # 计算核函数
    K = np.zeros((n_samples, n_samples))
    if sigma != 0:
        K = np.exp(-squareform(pdist(traindata, 'euclidean') * pdist(traindata, 'euclidean'))/(sigma * sigma))
        # for i in range(n_samples):
        #     for j in range(n_samples):
        #         K[i, j] = rbf_kernel(X[i], X[j], sigma)
    else:
        K = np.dot(X, X.T)
    print K.shape
    # 凸优化
    print 'opt....'
    P = cvxopt.matrix(np.outer(y, y) * K)
    q = cvxopt.matrix(np.ones(n_samples) * -1)
    A = cvxopt.matrix(y, (1, n_samples))
    b = cvxopt.matrix(0.0)

    tmp1 = np.diag(np.ones(n_samples) * -1)
    tmp2 = np.identity(n_samples)
    G = cvxopt.matrix(np.vstack((tmp1, tmp2)))
    tmp1 = np.zeros(n_samples)
    tmp2 = np.ones(n_samples) * C
    h = cvxopt.matrix(np.hstack((tmp1, tmp2)))

    # solve QP problem
    solution = cvxopt.solvers.qp(P, q, G, h, A, b)

    # Lagrange multipliers
    a = np.ravel(solution['x'])

    print 'predicting'
    # 得到支持向量
    sv0 = a > 1e-5
    ind = np.arange(len(a))[sv0]
    a = a[sv0]
    sv = X[sv0]
    sv_y = y[sv0]
    # print("%d support vectors out of %d points" % (len(a), n_samples))

    # 计算参数W和b
    b = 0
    for n in range(len(a)):
        b += sv_y[n]
        b -= np.sum(a * sv_y * K[ind[n], sv0])
    b /= len(a)

    # Weight vector
    w = None
    if sigma == 0:
        w = np.zeros(n_features)
        for n in range(len(a)):
            w += a[n] * sv_y[n] * sv[n]

    # 预测
    # testlabel = testlabel * 2 - 1
    if w is not None:
        y_predict = np.dot(testdata, w) + b
    else:
        y_predict = np.zeros(len(testdata))
        for i in range(len(testdata)):
            s = 0
            for a_, sv_y_, sv_ in zip(a, sv_y, sv):
                s += a_ * sv_y_ * rbf_kernel(testdata[i], sv_)
            y_predict[i] = s
        y_predict += b

    y_predict = ((np.sign(y_predict) + 1) / 2).astype(int)
    y_test = testlabel.astype(int)
    sp = 1.0 * sum(y_predict & y_test) / sum(y_predict)
    sr = 1.0 * sum(y_predict & y_test) / sum(y_test)
    f = (sr * sp * 2) / (sp + sr)
    # print sp, sr, f
    return f


print '[INFO]loading emails...'
spams, hams = load_data(5000)
spams, hams = mail_filter(spams), mail_filter(hams)
print '[INFO]preprocessing emails...'
# 预处理
spams = [preprocessing(spam) for spam in spams]
hams = [preprocessing(ham) for ham in hams]
# TDM
print '[INFO]building TDM...'
spam_tdm, ham_tdm = email_tdm(spams, hams)
# 划分数据集
print '[INFO]splitting data...'
print len(spam_tdm), len(ham_tdm)
x_trains, y_trains, x_tests, y_tests = data_split_5fold(spam_tdm, ham_tdm, 0.8)
print len(x_trains[0]), len(x_tests[0])


thresholds = np.array([0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9])
lambdas = np.array([1e-4, 0.01, 0.1, 0.5, 1, 5, 10, 100, 1000, 5000, 10000])
sigmas = np.array([0.01, 0.1, 1, 10, 100])
Cs = [1, 10, 100, 1000]

nb_f = np.zeros((len(thresholds), 5))
ls_f = np.zeros((len(lambdas), 5))
ss_f = np.zeros((len(sigmas) * len(Cs), 5))

for i in range(5):
    print '[INFO]training round: ' + str(i)
    # 朴素贝叶斯
    print '[INFO]naive bayes....'
    for j in range(len(thresholds)):
        f = nBayesClassifier(x_trains[i], y_trains[i], x_tests[i], y_tests[i], thresholds[j])
        nb_f[j, i] = f
    # 最小二乘法
    print '[INFO]least squares...'
    for j in range(len(lambdas)):
        f = lsClassifier(x_trains[i], y_trains[i], x_tests[i], y_tests[i], lambdas[j])
        ls_f[j, i] = f
    # 软边界支持向量机
    print '[INFO]SVM...'
    # 计算d
    d = 0.0
    for x in x_trains[i]:
        d += 1.0 * sum(sum((x_trains[i] - np.array(x)) * (x_trains[i] - np.array(x)))) / (len(x_trains[i]) * len(x_trains[i]))
    # 遍历svm的参数选择
    for j in range(len(Cs)):
        for k in range(len(sigmas)):
            f = softsvm(x_trains[i], y_trains[i], x_tests[i], y_tests[i], sigma=sigmas[k] * d, C=Cs[j])
            ss_f[j * len(sigmas) + k, i] = f
            print f

print '[RES]naive bayes F:'
print np.mean(nb_f, axis=1)
print '[RES]least squares F:'
print np.mean(ls_f, axis=1)
print '[RES]softsvm F:'
print np.mean(ss_f, axis=1)


