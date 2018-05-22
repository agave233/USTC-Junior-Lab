# -*- coding: utf-8 -*-
# lab5-PB15111662
# environment:python3.5

import math

def gauss_column_pivot(A, b):
	n = len(b)
	x = [0] * n
	for i in range(n - 1):
		# find maximum privot of column i
		max_a, k = math.fabs(A[i][i]), i
		for j in range(i + 1, n):
			if math.fabs(A[i][j]) > max_a:
				max_a, k = math.fabs(A[i][j]), j

		for j in range(i, n):
			A[i][j], A[k][j] = A[k][j], A[i][j]
		b[i], b[k] = b[k], b[i]

		for j in range(i + 1, n):
			t = A[j][i] / A[i][i]
			for r in range(i + 1, n):
				A[j][r] -= t * A[i][r]
			b[j] -= t * b[i]

	for i in range(n - 1, -1, -1):
		x[i] = b[i]
		for j in range(i + 1, n):
			x[i] -= A[i][j] * x[j]
		x[i] /= A[i][i]

	return x


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

x = gauss_column_pivot(A, b)
print('根为：')
for each in x:
	if each > 0:
		print(' %.15e' % each)
	else:
		print('%.15e' % each)
