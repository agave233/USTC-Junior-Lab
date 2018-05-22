# -*- coding: utf-8 -*-
# lab2-PB15111662
# environment:python2.7
# lagrange interpolation medthod
# based on Isometric segmentation and Chebyshev segmentation
import math


# f(x) = 1 / (1 + x^2)
def func(x):
    res = 1 / (1 + math.pow(x, 2))
    return res


# calculate lagrange for x
def calc_lagrange(x, x_set, n):
    res = 0
    for i in range(n + 1):
        lag = 1.0
        for j in range(n + 1):
            if i != j:
                lag *= (x - x_set[j]) / (x_set[i] - x_set[j])
        res += lag * func(x_set[i])
    return res


# Isometric segmentation:xi = -5 + (10 / n) * i
def isometric_segmentation(n):
    x_set = [-5.0 + (10.0 / n) * i for i in range(n + 1)]
    return x_set


# Chebyshev segmentation:xi = -5 * cos(((2 * i + 1) / (2 * n + 2)) * pi)
def chebyshev_segmentation(n):
    x_set = [-5 * math.cos(((2.0 * i + 1.0) / (2.0 * n + 2.0)) * math.pi) for i in range(n + 1)]
    return x_set


# lagrange interpolation medthod
def lagrange(n, x_set):
    max_error = 0
    for i in range(501):
        x = i / 50.0 - 5.0
        res = calc_lagrange(x, x_set, n)
        error = math.fabs(func(x) - res)
        if error > max_error:
            max_error = error
    return max_error


N = [5, 10, 20, 40]

# first get the set and return max error if lagrange
print "第一组节点，误差为："
for n in N:
    isometric_set = isometric_segmentation(n)
    res_error = lagrange(n, isometric_set)
    print 'n =', n, ',', '%.12e' % res_error

print "第二组节点，误差为："
for n in N:
    chebyshev_set = chebyshev_segmentation(n)
    res_error = lagrange(n, chebyshev_set)
    print 'n =', n, ',', '%.12e' % res_error
