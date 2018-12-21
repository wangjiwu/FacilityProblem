import time
import random

import numpy as np
#工厂数
n = 0
#客户数
m = 0
#工厂容量
capacity = []
#工厂建立花费
opening_cost = []
#客户需求
demand_customer = []
#客户和工厂的距离
assignment_cost = []


#  读取数据函数
def ReadData (examplenum) :
    f = open("Instances/p" + str(examplenum))

    i = 0
    demandRowCount = 0

    global n
    global m
    global assignment_cost
    global capacity
    global opening_cost
    global demand_customer
    opening_cost = []
    demand_customer = []
    capacity = []
    n = 0
    m = 0
    rowForSingleFac = 0
    try:
        for line in f:
            line = line.replace('\n', "")
            tmps = line.split(" ")
            tmp = []

            for item in tmps :
                if item != "":
                    tmp.append(item)

            if i == 0:

                n = int(tmp[0])
                m = int(tmp[1])
                rowForSingleFac = n // 10
                demandRowCount = m // 10
            elif i <= n:

                capacity.append(int(tmp[0]))
                opening_cost.append(int(tmp[1]))
            elif i <= n + demandRowCount:
                tmp = line.replace(".", "")
                tmp = tmp.split(" ")
                for item in tmp:
                    if item != "":
                        demand_customer.append(int(item))
            elif i <= n + demandRowCount + m * rowForSingleFac :
                tmpNum = []
                tmp = line.replace(".", " ")
                tmp = tmp.split(" ")
                for item in tmp:
                    if item != "":
                        tmpNum.append(int(item))

                assignment_cost.append(tmpNum)

            i = i + 1



        if rowForSingleFac != 1:
            for i in range (m):

                for j in range(1, rowForSingleFac):
                    assignment_cost[i] = assignment_cost[i] + assignment_cost[i * rowForSingleFac + j]

            assignment_cost = assignment_cost[0:m]

        f.close()
        #print("read success")

    except:

        #print("read failed")
        pass

# 返回每个用户的工厂排名（以用户的cost为计量单位）
def get_assign_rank (assign):

    rank_array = []


    for item in assignment_cost:

        # for x in range(n):
        #     item[x] = item[x] + opening_cost[x]


        tmp = sorted(item)
        addArr = []

        for i in range(n):
            addArr.append(tmp.index(item[i]))

        rank_array.append(addArr)

    return rank_array

# 贪心算法求解
def greedSingle():
    customer_assign = []
    #此解的 工厂开放费用和客户安排费用
    total_assign_cost = 0
    total_open_cost = 0

    #获取 每个客户的 对于每个工厂的排名矩阵
    # 每一行对应第i个矩阵
    # 没一列对于此工厂的在所有工厂的assign费用排名  优先选最小
    assignment_cost_rank = get_assign_rank(customer_assign)

    open_flag = []
    #初始化 工厂开放情况
    for x in range(n):
        open_flag.append(0)
    #
    for i in range(m):
        #对于每一个用户
        for j in range(n):
            # 找到当前 想要加入的工厂的下标
            try:
                #从排名为0 的工厂开始 把此工厂定义为 此用户要被安排进的工厂
                fac_num = assignment_cost_rank[i].index(j)
            except:
                fac_num = assignment_cost_rank[i].index(j + 1)
            # 如果此工厂能装得下
            if demand_customer[i] < capacity[fac_num]:

                if open_flag[fac_num] == 0:
                    open_flag[fac_num] = 1
                    total_open_cost += opening_cost[fac_num]

                # 则表示将当前用户安排给自工厂， 更新相应数据
                customer_assign.append(fac_num)
                total_assign_cost += assignment_cost[i][j]
                capacity[fac_num] = capacity[fac_num] - demand_customer[i]
                break
            else:
                pass
    # print(total_open_cost + total_assign_cost)
    # # print(total_assign_cost)
    # # print(total_open_cost)
    # print(open_flag)
    # # print(capacity)
    # print(customer_assign)


    return total_open_cost + total_assign_cost, open_flag,customer_assign

#生成随机解
def produce_randan_solution():


    #对于每个用户 随机分配到一个工厂

    factory_open = [0] * n
    customer_assign = []
    total_opening_cost = 0
    total_assignment_cost = 0
    demand_customer_copy = demand_customer.copy()
    capacity_copy = capacity.copy()

    for i in range(m) :
        #判断是否继续为此工厂挑选随机解
        flag = True
        fac_num = -1
        while (flag) :
            #生成随机数
            fac_num = random.randint(0, n - 1)

            #如果容量符合要求则选择该工厂
            if (demand_customer_copy[i] <= capacity_copy[fac_num]) :
                #如果工厂没开 则开工厂
                if (factory_open[fac_num] == 0) :
                    factory_open[fac_num] = 1
                    total_opening_cost += opening_cost[fac_num]
                #写入到安排计划数组里
                customer_assign.append(fac_num)
                #减去相应容量
                capacity_copy[fac_num] -= demand_customer_copy[i]
                #更新总共total_assignment_cost
                total_assignment_cost += assignment_cost[i][fac_num]
                #更新flag
                flag = False


    return total_opening_cost + total_assignment_cost, factory_open, customer_assign

#根据传入的解 生成一个局部的解, 并且求出此解的cost 当做参数传出
def produce_local_search_solution(bestFactoryOpen, bestValueAssign, capacity_copy):

    flag = True
    fac_num = -1
    #选择的随机顾客标号为i
    i = random.randint(0, m - 1)

    while (flag):
        # 生成被安排的随机工厂
        fac_num = random.randint(0, n - 1)
        #如果生成的随机工厂就是原来的工厂则继续生成
        if (fac_num == bestValueAssign[i]):
            continue

        # 如果容量符合要求则选择该工厂
        if (demand_customer[i] <= capacity_copy[fac_num]):
            # 如果工厂没开 则开工厂
            if (bestFactoryOpen[fac_num] == 0):
                bestFactoryOpen[fac_num] = 1


            #给离开的工厂加上相应的容量
            capacity_copy[bestValueAssign[i]] += demand_customer[i]
            #同时减去相应的assign消耗


            #如果离开的工厂的容量变为初始容量， 则把工厂设置为关闭
            if(capacity_copy[bestValueAssign[i]] == capacity[bestValueAssign[i]]):
                bestFactoryOpen[bestValueAssign[i]] = 0


            # 更新安排表
            bestValueAssign[i] = fac_num
            # 减去相应容量
            capacity_copy[fac_num] -= demand_customer[i]
            # 更新总共total_assignment_cost

            # 更新flag
            flag = False

        #计算此解的cost 当做参数传出去
        bestCost = 0
        for s in range(m):
            bestCost += assignment_cost[i][bestValueAssign[s]]

        for d in range(n):
            bestCost += bestFactoryOpen[d] * opening_cost[d]

    return bestCost,bestFactoryOpen, bestValueAssign, capacity_copy

#蒙特卡洛求解
def monte_carlo_search():

    bestValue = 1000000
    bestFactoryOpen = []
    bestValueAssign = []
    time_start = time.time()
    for i in range (10000) :


        tmp = produce_randan_solution()


        if (tmp[0] < bestValue):
            bestValue = tmp[0]
            bestFactoryOpen = tmp[1]
            bestValueAssign = tmp[2]
    time_end = time.time()
    # print(time_end - time_start)
    # print(bestValue)
    # print(bestFactoryOpen)
    # print(bestValueAssign)

    return bestValue, bestFactoryOpen, bestValueAssign

# 局部搜索求解
def local_search(i):

    tmp = greedSingle()

    bestCost = tmp[0]
    bestFactoryOpen = tmp[1]
    bestValueAssign = tmp[2]
    capacity_copy = capacity.copy()

    #因为进行贪心算法之后 全局数据发送了污染 所以要重新读取数据
    ReadData(i)

    for x in range(100000) :
        #生成局部新解
        tmp1 = produce_local_search_solution(bestFactoryOpen, bestValueAssign, capacity_copy)

        #如果新解优于原先解 则进行更新

        if tmp1[0] < bestCost:
            bestCost = tmp1[0]
            bestFactoryOpen = tmp1[1]
            bestValueAssign = tmp1[2]
            capacity_copy = tmp1[3]




    print (bestCost)

    print (bestFactoryOpen)

    print (bestValueAssign)

    return bestCost

# 模拟退火算法求解
def Simulate_Anneal(i) :
    #设置初始参数
    T0 = 1000
    Tmin = 1
    eta = 0.95
    #生成初始解 此解是贪心算法得到的
    tmp = greedSingle()

    bestCost = tmp[0]
    bestFactoryOpen = tmp[1]
    bestValueAssign = tmp[2]
    capacity_copy = capacity.copy()

    #因为进行贪心算法之后 全局数据发送了污染 所以要重新读取数据
    ReadData(i)
    t = T0

    while(t >= Tmin):

        #进行1000次生成新解的函数
        for j in range(1000):
            # 生成局部新解
            tmp1 = produce_local_search_solution(bestFactoryOpen, bestValueAssign, capacity_copy)

            # 如果新解优于原先解 则进行更新
            # 否则以一定的概率接受新解
            costDiffence = tmp1[0] - bestCost

            if tmp1[0] < bestCost or np.exp(-costDiffence/(t))>np.random.rand():

                bestCost = tmp1[0]
                bestFactoryOpen = tmp1[1]
                bestValueAssign = tmp1[2]
                capacity_copy = tmp1[3]

        t = eta*t
    #打印结果
    # print (bestCost)
    #
    # print (bestFactoryOpen)
    #
    # print (bestValueAssign)

    return bestCost


#贪心测试
def greedTest():

    for i in range(1,72):

        #67 这个数据有毒 是 以4个数据为一列 所以跳过此数据
        if i == 67:
            continue



        # 工厂数
        n = 0
        # 客户数
        m = 0
        # 工厂容量
        capacity = []
        # 工厂建立花费
        opening_cost = []
        # 客户需求
        demand_customer = []
        # 客户和工厂的距离
        assignment_cost = []

        print("=============================test" + str(i) + "=============================")

        strprint = ""

        strprint = strprint + "p" + str(i) + "|"
        time_start = time.time()
        ReadData(i)
        tmp = greedSingle()
        time_end = time.time()

        #strprint += str(tmp) + "|" + str(time_end-time_start)[0:8]



        #print(strprint)

        if n == 0 :
            break

#蒙特卡洛测试
def monte_carlo_test():


    for i in range(1,72):

        #67 这个数据有毒 是 以4个数据为一列 所以跳过此数据
        if i == 67:
            continue



        # 工厂数
        n = 0
        # 客户数
        m = 0
        # 工厂容量
        capacity = []
        # 工厂建立花费
        opening_cost = []
        # 客户需求
        demand_customer = []
        # 客户和工厂的距离
        assignment_cost = []

        print("=============================test" + str(i) + "=============================")

        strprint = ""

        strprint = strprint + "p" + str(i) + "|"
        time_start = time.time()
        ReadData(i)
        tmp = monte_carlo_search()
        time_end = time.time()

        strprint += str(tmp[0]) + "|" + str(time_end-time_start)[0:8]
        print(tmp[0])
        print(tmp[1])
        print(tmp[2])


        #print(strprint)

        if n == 0 :
            break

#局部搜索测试
def local_search_test():

    for i in range(1,72):

        #67 这个数据有毒 是 以4个数据为一列 所以跳过此数据
        if i == 67:
            continue

        global n
        global m
        global assignment_cost
        global capacity
        global opening_cost
        global demand_customer

        # 工厂数
        n = 0
        # 客户数
        m = 0
        # 工厂容量
        capacity = []
        # 工厂建立花费
        opening_cost = []
        # 客户需求
        demand_customer = []
        # 客户和工厂的距离
        assignment_cost = []

        print("=============================test" + str(i) + "=============================")

        strprint = ""

        strprint = strprint + "p" + str(i) + "|"
        time_start = time.time()
        ReadData(i)
        tmp = local_search(i)
        time_end = time.time()

        strprint += str(tmp) + "|" + str(time_end-time_start)[0:8]
        # print(tmp[0])
        # print(tmp[1])
        # print(tmp[2])


        #print(strprint)

# 模拟退火测试
def Simulate_Anneal_test() :
    for i in range(1, 72):

        # 67 这个数据有毒 是 以4个数据为一列 所以跳过此数据
        if i == 67:
            continue

        global n
        global m
        global assignment_cost
        global capacity
        global opening_cost
        global demand_customer

        # 工厂数
        n = 0
        # 客户数
        m = 0
        # 工厂容量
        capacity = []
        # 工厂建立花费
        opening_cost = []
        # 客户需求
        demand_customer = []
        # 客户和工厂的距离
        assignment_cost = []

        #print("=============================test" + str(i) + "=============================")

        strprint = ""

        strprint = strprint + "p" + str(i) + "|"
        time_start = time.time()
        ReadData(i)
        tmp = Simulate_Anneal(i)
        time_end = time.time()

        strprint += str(tmp) + "|" + str(time_end - time_start)[0:8]
        # print(tmp[0])
        # print(tmp[1])
        # print(tmp[2])

        print(strprint)




if __name__ == '__main__':
    Simulate_Anneal_test()


     # ReadData(1)
     # Simulate_Anneal(1)
