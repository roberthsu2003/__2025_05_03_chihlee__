#常態分佈(高斯分佈)
import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt
from scipy.stats import norm  # 用於計算常態分佈的PDF

normal_ditribution:ndarray = np.random.normal(loc=80,scale=0.1,size=(50))
plt.hist(normal_ditribution, bins=30, color='#B47157',alpha=0.5)
# 計算x軸範圍
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
# 計算對應x的常態分佈機率密度值
p = norm.pdf(x, loc=np.mean(normal_ditribution), scale=np.std(normal_ditribution))
plt.plot(x, p, color='red' ,linewidth=2)
print(x)
plt.show()