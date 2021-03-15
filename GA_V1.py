#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ga.py
# @Author  : JinH
# @Date    : 2019/7/9/14:17
# @Version : Python_3.7
# @SoftWare: PyCharm
# @Desc    :


import matplotlib.pyplot as plt
import numpy as np
import math


# ↓ 适应度函数
def fitness(x):
    return x + 10 * np.sin(5 * x) + 7 * np.cos(4 * x)
    #return x * np.sin(10 * math.pi * x)


# ↓ 个体类
class individual:
    def __init__(self):
        # ↓ 染色体编码
        self.x = 0
        # ↓ 适应度值
        self.fitness = 0

    def __eq__(self, other):
        self.x = other.x
        self.fitness = other.fitness


# ↓ 初始化种群
def initPopulation(pop, N):
    for i in range(N):
        ind = individual()
        ind.x = np.random.uniform(-10, 10)
        ind.fitness = fitness(ind.x)
        pop.append(ind)


# ↓ 选择过程
def selection(N):
    # ↓ 种群中随机选取2个个体进行变异，没有使用轮盘赌，而是直接随机选择
    return np.random.choice(N, 2)


# ↓ 结合/交叉过程
def crossover(parent1, parent2):
    child1, child2 = individual(), individual()
    child1.x = 0.9 * parent1.x + 0.1 * parent2.x
    child2.x = 0.1 * parent1.x + 0.1 * parent2.x
    child1.fitness = fitness(child1.x)
    child2.fitness = fitness(child2.x)
    return child1, child2


# ↓ 变异过程
def mutation(pop):
    # ↓ 种群中随便选择一个进行变异
    ind = np.random.choice(pop)
    # ↓ 用随机赋值的方式进行变异
    ind.x = np.random.uniform(-10, 10)
    ind.fitness = fitness(ind.x)


# ↓ 最终执行
def implement():
    # ↓ 种群中个体的数量
    N = 100
    # ↓ 种群
    POP = []
    # ↓ 迭代次数
    iter_N = 500
    # ↓ 初始化种群
    initPopulation(POP, N)
    # ↓ 进化过程
    for it in range(iter_N):
        a, b = selection(N)
        # ↓ 以0.75的概率进行交叉结合
        if np.random.random() < 0.75:
            child1, child2 = crossover(POP[a], POP[b])
            new = sorted([POP[a], POP[b], child1, child2],
                         key=lambda ind: ind.fitness, reverse=True)
            POP[a], POP[b] = new[0], new[1]

        # ↓ 以0.1的概率进行变异
        if np.random.random() < 0.1:
            mutation(POP)

        POP.sort(key=lambda ind: ind.fitness, reverse=True)

    return POP


# ↓ 图像展示
def showDetail(pop):
    x = np.linspace(-10, 10, 10000)
    y = fitness(x)
    scatter_x = np.array([ind.x for ind in pop])
    scatter_y = np.array([ind.fitness for ind in pop])
    plt.plot(x, y)
    plt.scatter(scatter_x, scatter_y, c='r')
    plt.title('个体数量：%s' % len(pop))
    plt.show()


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    pop = implement()
    showDetail(pop)