# -*- coding: utf-8 -*-
# lab6-PB15111662
# environment:python3.5

from math import fabs


def gauss_seidel(A, b, eps):
	n, error, k = len(A), 1, 0
	x2 = [1.0] * n
	while error > eps:
		k += 1
		x1 = [each for each in x2]
		for i in range(n):
			t = sum([A[i][j] * x2[j] if j != i else 0.0 for j in range(n)])
			x2[i] = -(t - b[i]) / A[i][i]
		error = max([fabs(x1[i] - x2[i]) for i in range(n)])
	return x2, k


def sor(A, b, omega, eps):
	n, error, k = len(A), 1, 0
	x2 = [1.0] * n
	while error > eps:
		k += 1
		x1 = [each for each in x2]
		for i in range(n):
			t = sum([A[i][j] * x2[j] if j != i else 0.0 for j in range(n)])
			t = -(t - b[i]) / A[i][i]
			x2[i] = (1 - omega) * x2[i] + omega * t
		error = max([fabs(x1[i] - x2[i]) for i in range(n)])
	return x2, k




A = [[31, -13, 0, 0, 0, -10, 0, 0, 0],
	 [-13, 35, -9, 0, -11, 0, 0, 0, 0],
	 [0, -9, 31, -10, 0, 0, 0, 0, 0],
	 [0, 0, -10, 79, -30, 0, 0, 0, -9],
	 [0, 0, 0, -30, 57, -7, 0, -5, 0],
	 [0, 0, 0, 0, -7, 47, -30, 0, 0],
	 [0, 0, 0, 0, 0, -30, 41, 0, 0],
	 [0, 0, 0, 0, -5, 0, 0, 27, -2],
	 [0, 0, 0, -9, 0, 0 ,0, -2, 29]]
b = [-15, 27, -23, 0, -20, 12, -7, 7, 10]


root, k = gauss_seidel(A, b, 1e-6)
best_w, min_step = 0, float("inf")
print('根为:')
# print('\n'.join(map(str, root)))
for each in root:
	print(' %.15e' % each)
print('Gauss-seidel迭代总迭代步数为:', k)
print('SOR迭代步数为:')
for i in range(1, 100):
	r, k =sor(A, b, i / 50.0, 1e-6)
	if r[0] != r[0]:
		print('松弛因子:', '%.2f,' % (i / 50.0), "不收敛")
	else:
		best_w = i / 50.0 if min_step > k else best_w 
		min_step = min(min_step, k)
		print('松弛因子:', '%.2f,' % (i / 50.0), k)

print("取松弛因子为", best_w, "时最佳, 步数为", min_step)



# 实验分析与思考
# 在本实验中分别用Gauss-Seidel和SOR方法对矩阵进行迭代求解
# 说明：选用的误差界限为1e-6，初始值为[1,...,1]
# 通过实验结果来看，Gauss-Seidel法需要22步的迭代过程。且由于该矩阵对称正定，所以保证收敛，并且实际结果也得到正确解
# 而SOR迭代法当选取不同的w时，其迭代速度也有所不同，w从较小值开始逐渐增大时，其收敛速度先变快然后减慢。并且在w接近于
# 2时，SOR迭代法不收敛。
# 分析可知，在w很小的时候，由Gauss-Seidel求得的部分占比例小，而每一轮迭代过程x的更新幅度很小，所以此时收敛速度慢
# 然后随着w增大，解的更新的幅度变大，收敛速度加快，当w=1时即为Gauss-Seidel法，但是在w增大到某一个值继续增大时，
# 由于其迭代矩阵谱半径增大而收敛速度减慢，以至于在普半径大于1时会导致不收敛。
# 所以，SOR迭代方法中松弛因子的取值直接影响到算法的收敛性及收敛速度。若选择得当，可以加快收敛速度。