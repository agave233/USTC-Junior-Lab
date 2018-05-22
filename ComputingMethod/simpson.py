# -*- coding: utf-8 -*-
# lab3-PB15111662
# environment:python3.6

from math import *


# 复化梯形积分
def trapezoid(a, b, n):
	h = (b - a) / n
	res = (sin(a) + sin(b)) / 2
	for i in range(1, n):
		res += sin(a + i * h)
	return h * res

# 复化simpson积分
def simpson(a, b, n):
	m = int(n / 2)
	h = (b - a) / n
	res = (sin(a) + sin(b)) / 3

	for i in range(m):
		res += 4 * sin(a + (2 * i + 1) * h) / 3
	for i in range(1, m):
		res += 2 * sin(a + 2 * i * h) / 3

	return h * res


a, b = 1.0, 5.0
real_res = cos(a) - cos(b)

print('复化梯形积分公式的误差和误差阶为：')
for k in range(13):
	n = int(pow(2, k))
	res_h = trapezoid(a, b, n)
	res_2h = trapezoid(a, b, n * 2)
	error_h = fabs(res_h - real_res)
	error_2h = fabs(res_2h - real_res)
	error_order = log(error_h / error_2h) / log(2)
	# print 'N = %-4d' % n , '，%.12e' % error_h, '，', '%.12e' % error_order
	print('N = %-4d' % n + '，%.15e' % error_h + '，%.15e' % error_order)


print('复化Simpson积分公式的误差和误差阶为：')
for k in range(13):
	n = int(pow(2, k))
	res_h = simpson(a, b, n)
	res_2h = simpson(a, b, n * 2)
	error_h = fabs(res_h - real_res)
	error_2h = fabs(res_2h - real_res)
	error_order = log(error_h / error_2h) / log(2)
	print('N = %-4d' % n + '，%.15e' % error_h + '，%.15e' % error_order)
	# print 'N = %-4d' % n, '，%.12e' % error_h, '，', '%.12e' % error_order


# 关于实验的分析与思考
# 1。
# 该实验是分别用复化梯形和复化simpson积分求解，通过结果可以看到随着
# 我们的间隔数N越大，也就是步长越短时，得到的结果误差越小，这是因为
# 在步长变小时，我们把曲线划分的每个区域越来越小，对其进行梯形或者
# simpson的近似求解时越来约逼近真实的结果，这样总的积分值的误差也就
# 越来越小。
# 2。
# 每一步求解的精度保留对最终的积分结果很重要。一开始我用的是python2.7
# 其默认的浮点数运算精度为12位，执行的结果误差比用pyhton2.7的误差略微
# 大一点，所以在计算时也应该考虑计算精度的问题。
