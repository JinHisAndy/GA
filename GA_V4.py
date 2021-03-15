#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : GA_V4.py
# @Author  : JinH
# @Date    : 2019/7/18/15:43
# @Version : Python_3.7
# @SoftWare: PyCharm
# @Desc    : 


import numpy as np


# ↓ 适应度函数
def fitness(x):
    return np.sin(x[0]) * np.cos(x[1]) * np.tan(x[2]) - np.sqrt(x[0] ** 2 + x[1] ** 2 + x[2] ** 2) / 2


# ↓ 个体类
class individual:
    def __init__(self):
        # ↓ 染色体编码
        self.x = np.array([np.random.uniform(-10, 10), np.random.uniform(-10, 10), np.random.uniform(-10, 10)])
        # ↓ 适应度值
        self.fitness = fitness(self.x)

    def __eq__(self, other):
        self.x = other.x
        self.fitness = other.fitness


# ↓ 初始化种群
def initPopulation(pop, N):
    for i in range(N):
        ind = individual()
        pop.append(ind)


# ↓ 结合/交叉过程
def crossover(parent1, parent2, variation_rate, Now, All):
    child1, child2 = individual(), individual()
    child1.x = 0.9 * parent1.x + 0.1 * parent2.x
    # ↓ 新生儿几率性发生变异
    if np.random.random() < variation_rate:
        bias = 1 - Now / All
        child1 = mutation(child1, bias)

    child2.x = 0.1 * parent1.x + 0.1 * parent2.x
    # ↓ 新生儿几率性发生变异
    if np.random.random() < variation_rate:
        bias = 2 - (Now / All) * 2
        child2 = mutation(child2, bias)

    child1.fitness = fitness(child1.x)
    child2.fitness = fitness(child2.x)
    return child1, child2


# ↓ 变异过程
def mutation(ind, bias):
    # ↓ 个体发生变异，步长最长为1，方向随机
    direction = np.random.random() * np.pi
    ind.x[0] = ind.x[0] + bias * np.cos(direction)
    ind.x[1] = ind.x[1] + bias * np.sin(direction)
    ind.x[2] = ind.x[2] + bias * np.tan(direction)
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
def born(pop, born_rate, variation_rate, Now, All):
    # ↓ 根据适应度排序
    sort(pop)
    # ↓ 优秀的一部分获得生育权
    couldBorn = pop[:int((len(pop) / (1 - born_rate) * born_rate))]
    for i in range(0, len(couldBorn), 2):
        # ↓ 每队夫妇生育二个后代，维持种群内个体总数不变
        child1, child2 = crossover(
            couldBorn[i], couldBorn[i + 1], variation_rate, Now, All)
        pop.append(child1)
        pop.append(child2)
    return pop


# ↓ 最终执行
def implement(N, iter_N, killOrborn_rate, variation_rate):
    '''
    :param N: 种群中个体的数量
    :param iter_N: 繁殖代数
    :param killOrborn_rate: 淘汰比率/出生比率
    :param variation_rate: 变异率
    :return:
    '''
    POP = []
    # ↓ 初始化种群
    initPopulation(POP, N)
    # ↓ 进化过程
    for it in range(iter_N):
        # ↓ 淘汰掉不适应环境的一部分
        POP = kill(POP, killOrborn_rate)
        # ↓ 适应环境的一部分择优进行繁殖
        POP = born(POP, killOrborn_rate, variation_rate, it, iter_N)
        # showDetail(POP, it + 1, iter_N)
    sort(POP)
    return POP


if __name__ == '__main__':
    N = 20
    iter_N = 50
    killOrborn_rate = 0.5
    variation_rate = 0.5
    pop = implement(N, iter_N, killOrborn_rate, variation_rate)
    for each in pop:
        print('x1=%f,x2=%f,x3=%f\ty=%f' % (each.x[0], each.x[1], each.x[2], each.fitness))
    print('最优解  x1=%f,x2=%f,x3=%f  y=%f' % (pop[0].x[0], pop[0].x[1], pop[0].x[2], pop[0].fitness))
