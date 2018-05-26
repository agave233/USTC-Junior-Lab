 #-*- coding:utf-8 -*-
import matplotlib.pyplot as plt

f = open('pos.txt')
line = f.readline().rstrip()
x, y = [], []
while line:
	x.append(int(line.split(',')[0]))
	y.append(int(line.split(',')[1]))
	line = f.readline().rstrip()
plt.plot(x, y)
plt.savefig("plot.jpg")
plt.show()