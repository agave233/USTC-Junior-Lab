from math import sqrt
TIMES = 1000000


def hamming(x):
	res = 0
	for k in range(1,TIMES):
		res += 1 / (k * (k + x))
	return res


x_set = [0.0,0.5,1.0,sqrt(2),10.0,100.0,300.0]
for x in x_set:
	psix = hamming(x)
	print '%6.2f' % x,',','%16.12e' % psix