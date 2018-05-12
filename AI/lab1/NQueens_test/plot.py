# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style("whitegrid")
sns.set( palette="muted", color_codes=True)  
plt.rcParams['font.sans-serif']=['SimHei'] 
plt.rcParams['axes.unicode_minus']=False

n = ["10", "100", "1k", "1w", "3w", "5w", "8w", "10w", "30w", "50w", "80w", "100w"]

hc_m_0 = [0, 0.03125, 0, 0.015625, 0.046875, 0.078125, 0.0140625, 0.25, 1.28125, 2.8125, 3.98438,4.96875]
hc_m_n8 = [0, 0, 0, 0.015625, 0.046875, 0.078125, 0.375, 0.359375, 4.6875, 2.29688, 16.3438,30.1094]
hc_m_n4 = [0, 0, 0, 0, 0.09375, 0.125, 0.265625, 0.3125, 5.9375, 8.75, 25.3281,40.6719]
hc_m_n2 = [0, 0, 0, 0.015625, 0.078125, 0.09375, 0.25, 0.84375, 2.98438,13.8281,28.9531,36.4531]

sa_m_0 = [0, 0, 0, 0.015625, 0.046875, 0.140625, 0.203125, 0.296875, 1.59375, 2.89062, 4.5625, 5.125]
sa_m_n8 = [0, 0, 0, 0.015625, 0.0625, 0.15625, 0.578125, 0.53125, 3.76562, 3.1875, 21.4531, 22.6562]
sa_m_n4 = [0, 0, 0, 0.015625, 0.21875, 0.203125, 0.390625, 0.34375, 7.10938, 10.3594, 31.9062, 37.375]
sa_m_n2 = [0, 0, 0, 0.015625, 0.125, 0.125, 0.421875, 1.09375, 3.01562, 16.7344, 33.5781, 40.0469]

# plt.figure(figsize=(12,8))


def plot_hc():
	plt.figure(figsize=(8,6))
	plt.subplot(2,2,1)
	plt.plot(range(12), hc_m_0, alpha = 1, color = 'r', label = 'm = 0')
	plt.xticks(range(12), n)
	plt.ylabel('time/s', fontsize = 14)
	plt.legend()
	plt.subplot(2,2,2)
	plt.plot(range(12), hc_m_n8, alpha = 1, color='b', label = 'm = n/8')
	plt.xticks(range(12), n)
	plt.legend()
	plt.subplot(2,2,3)
	plt.plot(range(12), hc_m_n4, alpha = 1, color='g', label = 'm = n/4')
	plt.xticks(range(12), n)
	plt.legend()
	plt.subplot(2,2,4)
	plt.plot(range(12), hc_m_n2, alpha = 1, color='y', label = 'm = n/2')
	plt.xticks(range(12), n)
	plt.legend()
	plt.suptitle('爬山算法所用时间与m、n的曲线图', fontsize = 12)
	plt.xlabel('n', fontsize = 14)
	plt.xticks(horizontalalignment = 'right') 
	plt.savefig("hc_times.png")
	plt.show()

def plot_sa():
	plt.figure(figsize=(8,6))
	plt.subplot(2,2,1)
	plt.plot(range(12), sa_m_0, alpha = 1, color = 'r', label = 'm = 0')
	plt.xticks(range(12), n)
	plt.ylabel('time/s', fontsize = 14)
	plt.legend()
	plt.subplot(2,2,2)
	plt.plot(range(12), sa_m_n8, alpha = 1, color='b', label = 'm = n/8')
	plt.xticks(range(12), n)
	plt.legend()
	plt.subplot(2,2,3)
	plt.plot(range(12), sa_m_n4, alpha = 1, color='g', label = 'm = n/4')
	plt.xticks(range(12), n)
	plt.legend()
	plt.subplot(2,2,4)
	plt.plot(range(12), sa_m_n2, alpha = 1, color='y', label = 'm = n/2')
	plt.xticks(range(12), n)
	plt.legend()
	plt.suptitle('模拟退火算法所用时间与m、n的曲线图', fontsize = 12)
	plt.xlabel('n', fontsize = 14)
	plt.xticks(horizontalalignment = 'right') 
	plt.savefig("sa_times.png")
	plt.show()



plot_sa()
plot_hc()