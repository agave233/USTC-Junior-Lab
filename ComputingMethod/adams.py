# -*- coding: utf-8 -*-
# lab7-PB15111662
# environment:python3.5

import math

def func(x, y):

	return -1.0 * x * x * y * y


def runge_cutta(xm, xn, h, y0):

	l = int((xn - xm) / h)
	y = [y0]
	for i in range(l):
		xn = xm + i * h
		yn = y[-1]
		k1 = func(xn, yn)
		k2 = func(xn + h / 2.0, yn + h * k1 / 2.0)
		k3 = func(xn + h / 2.0, yn + h * k2 / 2.0)
		k4 = func(xn + h, yn + h * k3)
		yn += h * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
		y.append(yn)

	return y [-1] 



def adams_3(xm, xn, h, y0):

	y_n = y0
	yn = runge_cutta(xm, xm + h, h, y0)
	l = int((xn - xm) / h)

	for i in range(1, l):
		x_n = xm + (i - 1) * h
		xn = xm + i * h
		xn_ = xm + (i + 1) * h

		f_n = func(x_n, y_n)
		fn = func(xn, yn)
		error, yn_ = float('INF'), 0.0
		while error > 1e-6:
			t = yn_
			fn_ = func(xn_, yn_)
			yn_ = yn + h * (5 * fn_ + 8 * fn - f_n) / 12.0
			error = math.fabs(t - yn_)

		y_n, yn = yn, yn_

	return yn_


h_set = [0.1, 0.1 / 2, 0.1 / 4, 0.1 / 8]
xm, xn = 0.0, 1.5
y0, yn = 3.0, 3.0 / (1.0 + 1.5 * 1.5 * 1.5)
error_h = 0.0

print("Runge-Cutta:")
for h in h_set:
	res_h = runge_cutta(xm, xn, h, y0)
	res_h_2 = runge_cutta(xm, xn, h / 2.0, y0)
	error_h = math.fabs(res_h - yn)
	error_h_2 = math.fabs(res_h_2 - yn)
	error_order = math.log(error_h / error_h_2) / math.log(2)
	print("步长：", h, ", %.15e" % error_h, ",", error_order)
	# if h == h_set[0]:
	# 	error_h = error
	# 	print("步长：", h, ",", error, ",")
	# else:
	# 	error_order = math.log(error_h / error) / math.log(int(h_set[0] / h))
	# 	print("步长：", h, ",", error, ",", error_order)


print("Adams:")
for h in h_set:
	res_h = adams_3(xm, xn, h, y0)
	res_h_2 = adams_3(xm, xn, h / 2.0, y0)
	error_h = math.fabs(res_h - yn)
	error_h_2 = math.fabs(res_h_2 - yn)
	error_order = math.log(error_h / error_h_2) / math.log(2)
	print("步长：", h, ", %.15e" % error_h, ",", error_order)
	# res = adams_3(xm, xn, h, y0)
	# error = math.fabs(res - yn)
	# if h == h_set[0]:
	# 	error_h = error
	# 	print("步长：", h, ",", error, ",")
	# else:
	# 	error_order = math.log(error_h / error) / math.log(int(h_set[0] / h))
	# 	print("步长：", h, ",", error, ",", error_order)



# 实验结果分析与思考
# 三阶Adams每个y迭代求解时的误差界限说明：设定为1e-6
# 误差阶的说明：我采用的误差阶计算是之前老师在上课时说明的误差阶，对于实验要求的每一个h、，求e(h)对e(h/2)的误差阶，这样在程序每一个h都有误差阶，结果如上所示。
# 实验结果分析：本次实验中求解微分方程时，采用的是四阶Runge-Cutta和3阶隐式adams，从结果来看，可以得到以下结论分析：
# 1.对比四阶Runge-Cutta法和三阶adams法，在相同步长h下，Runge-Cutta的误差小于adams法，求解的精度较高，这是因为根据泰勒展开，四阶的Runge-Cutta的误差界为O(h^5),
# 而三阶隐式adams的误差界为O(h^4)，所以采用四阶Runge-Cutta的效果更好。
# 2.对于每一种方法而言，步长越短模拟的结果更为准确，这是显然的结论，因为步长越短对于原方程的解的拟合程度越高所以结果更好。
# 总结：在用数值方法求解微分方程时，线性多步法和Runge-Cutta都可以达到较好的结果，并且adams法在隐式情况下需要用结合Runge-Cutta进行起步计算，在实现时还要考虑迭代的
# 误差界限和步长选择等多种情况来综合考虑计算代价以及结果的精确性。