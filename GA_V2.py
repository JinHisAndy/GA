#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ga.py
# @Author  : JinH
# @Date    : 2019/7/9/19:47
# @Version : Python_3.7
# @SoftWare: PyCharm
# @Desc    :


import matplotlib.pyplot as plt
import numpy as np
import math


# ↓ 适应度函数
def fitness(x):
    return x + 10 * np.sin(5 * x) + 7 * np.cos(4 * x)
    # return (np.cos(np.sin(x))) * (np.sin(2 * x) - 5 * np.cos(math.pi * x))
    # return np.sin(x)


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
def initPopulation(pop, N, iter_N):
    for i in range(N):
        ind = individual()
        ind.x = np.random.uniform(-10, 10)
        ind.fitness = fitness(ind.x)
        pop.append(ind)
    showDetail(pop, 0, iter_N)


# ↓ 结合/交叉过程
def crossover(parent1, parent2, variation_rate, Now, All, step):
    child1, child2 = individual(), individual()
    child1.x = 0.9 * parent1.x + 0.1 * parent2.x
    # ↓ 新生儿几率性发生变异
    if np.random.random() < variation_rate:
        bias = 1 - Now / All
        child1 = mutation(child1, bias, step)

    child2.x = 0.1 * parent1.x + 0.1 * parent2.x
    # ↓ 新生儿几率性发生变异
    if np.random.random() < variation_rate:
        bias = 2 - (Now / All) * 2
        child2 = mutation(child2, bias, step)

    child1.fitness = fitness(child1.x)
    child2.fitness = fitness(child2.x)
    return child1, child2


# ↓ 变异过程
def mutation(ind, bias, step):
    # ↓ 个体发生变异，步长为0.3，方向随机
    new_x = ind.x + bias * (np.random.choice([-1, 1])) * step
    if -10 < new_x < 10:
        ind.x = new_x
    return ind


# ↓ 根据适应度进行排序
def sort(pop):
    return pop.sort(key=lambda ind: ind.fitness, reverse=True)


# ↓ 淘汰过程
def kill(pop, kill_rate):
    # ↓ 根据适应度排序
    sort(pop)
    # ↓ 根据淘汰比例淘汰掉最不适应的一部分
    new_pop = pop[:int((len(pop) * (1 - kill_rate)))]
    return new_pop


# ↓ 生育过程
def born(pop, born_rate, variation_rate, Now, All, step):
    # ↓ 根据适应度排序
    sort(pop)
    # ↓ 优秀的一部分获得生育权
    couldBorn = pop[:int((len(pop) / (1 - born_rate) * born_rate))]
    for i in range(0, len(couldBorn), 2):
        # ↓ 每队夫妇生育二个后代，维持种群内个体总数不变
        child1, child2 = crossover(
            couldBorn[i], couldBorn[i + 1], variation_rate, Now, All, step)
        pop.append(child1)
        pop.append(child2)
    return pop


# ↓ 最终执行
def implement(N, iter_N, killOrborn_rate, variation_rate, step):
    '''
    :param N: 种群中个体的数量
    :param iter_N: 繁殖代数
    :param killOrborn_rate: 淘汰比率/出生比率
    :param variation_rate: 变异率
    :return:
    '''
    POP = []
    # ↓ 初始化种群
    initPopulation(POP, N, iter_N)
    # ↓ 进化过程
    for it in range(iter_N):
        # ↓ 淘汰掉不适应环境的一部分
        POP = kill(POP, killOrborn_rate)
        # ↓ 适应环境的一部分择优进行繁殖
        POP = born(POP, killOrborn_rate, variation_rate, it, iter_N, step)
        showDetail(POP, it + 1, iter_N)
    sort(POP)
    return POP


# ↓ 图像展示
def showDetail(pop, stage, iter_N):
    x = np.linspace(-10, 10, 10000)
    y = fitness(x)
    scatter_x = np.array([ind.x for ind in pop])
    scatter_y = np.array([ind.fitness for ind in pop])
    plt.plot(x, y)
    plt.scatter(scatter_x, scatter_y, c='r')
    plt.title('第%d轮进化，共%d轮。个体数量：%s' % (stage, iter_N, len(pop)))
    plt.show()


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    N = 100
    iter_N = 30
    killOrborn_rate = 0.2
    variation_rate = 0.3
    step = 0.3
    pop = implement(N, iter_N, killOrborn_rate, variation_rate, step)
    print(len(pop))
    for each in pop:
        print('x=%f\ty=%f' % (each.x, each.fitness))
    print('最优解 x=%f, y=%f' % (pop[0].x, pop[0].fitness))
    showDetail(pop, iter_N, iter_N)
