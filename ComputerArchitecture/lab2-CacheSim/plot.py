# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style("whitegrid")
sns.set( palette="muted", color_codes=True)  
plt.rcParams['font.sans-serif']=['SimHei'] 
plt.rcParams['axes.unicode_minus']=False

cache_sizes = ['2KB', '8KB', '32KB', '128KB', '512KB', '2MB']
map_methods = ['直接映像', '2路', '4路', '8路', '16路', '32路']
block_sizes = ['16B', '32B', '64B', '128B', '256B']
replace = ['         (8KB.32B,4路)', '         (32KB.64B,4路)', '        (8KB.32B,8路)']

miss_rate11 = [12.97, 10.41, 0.89, 0.22, 0.15, 0.15]
miss_rate12 = [11.36, 4.5, 0.78, 0.17, 0.1, 0.1]
miss_rate2 = [4.62, 2.76, 1.9, 1.65, 1.66, 1.68]
miss_rate3 = [5.74, 4.62, 4.35, 4.50, 5.15]
miss_rate41 = [3.05, 0.55, 2.83]
miss_rate42 = [3.37, 0.63, 3.16]
miss_rate43 = [11.99, 5.06, 16.29]
# plt.figure(figsize=(12,8))
def plot_cache_sizes():
	sns.pointplot(cache_sizes, miss_rate11, alpha = 0.8, color = 'r', label = '块大小64B')
	sns.pointplot(cache_sizes, miss_rate12, alpha=0.8, color='b', label = '块大小128B')
	plt.title('Cache 容量对不命中率的影响', fontsize = 14)
	plt.xlabel('Cache大小', fontsize = 14)
	plt.ylabel('不命中率(%)', fontsize = 14)
	plt.xticks(horizontalalignment = 'right') 
	plt.legend()
	plt.savefig("img/cache_sizes.png")
	plt.show()

def plot_map_methods():
	sns.pointplot(map_methods, miss_rate2, alpha = 0.8, color = 'r')
	plt.title('Cache 采取的映射机制对不命中率的影响', fontsize = 14)
	plt.xlabel('映射机制', fontsize = 14)
	plt.ylabel('不命中率(%)', fontsize = 14)
	plt.xticks(horizontalalignment = 'right') 
	plt.savefig("img/map_methods.png")
	plt.show()

def plot_block_sizes():
	sns.pointplot(block_sizes, miss_rate3, alpha = 0.8, color = 'r')
	plt.title('Cache 块大小对不命中率的影响', fontsize = 14)
	plt.xlabel('块大小', fontsize = 14)
	plt.ylabel('不命中率(%)', fontsize = 14)
	plt.xticks(horizontalalignment = 'right') 
	plt.savefig("img/block_sizes.png")
	plt.show()

def plot_replace():
	width = 0.25
	x = np.arange(3)
	plt.bar(x, miss_rate41, width = width, color = 'r', label = 'LRU')
	plt.bar(x + width, miss_rate42, width = width, color = 'm', label = 'FIFO')
	plt.bar(x + width * 2, miss_rate43, width = width, color = 'b', label = 'RAND')
	plt.title('Cache替换算法对不命中率的影响', fontsize = 14)
	plt.xlabel('替换算法', fontsize = 14)
	plt.ylabel('不命中率(%)', fontsize = 14)
	plt.xticks(x, replace) 
	plt.legend()
	plt.savefig("img/replace.png")
	plt.show()


plot_cache_sizes()
plot_map_methods()
plot_block_sizes()
plot_replace()