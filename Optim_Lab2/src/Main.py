import numpy as np
import random as rnd


way_matrix = np.load("C:/Users/Alexander/PythonProjects/PycharmProjects/"
                     "OptimizationMethods/Optim_Lab2/data/Task3.npy")

# print(way_matrix)

# создание двумерного списка феромонов
ti = [[0 for i in range(len(way_matrix))] for j in range(len(way_matrix))]
# print(ti)

k = 0.95

n_fer = 50 # феромон на маршрут
N = 100  # количество муравьев в популяции
start_point = 0 # начальная точка


def colony(way_matrix):


    ti = [[0 for i in range(len(way_matrix))] for j in range(len(way_matrix))]

    n_towns = len(ti[0])  # количество городов
    delta_ti = [[0 for i in range(n_towns)] for j in range(n_towns)]  # приращение
    alfa = 1
    betta = 1

    def __is__(way, t_way, wway, tt, alfa, betta):
        """ возвращает значение True или False в зависимости от выпадения
        монетки """
        summ = 0

        for i in wway:
            if i == 0 : wway.remove(0)

        for i in range(len(wway)):
            summ += tt[i]**alfa + 1/(wway[i]**betta)

        probability = (t_way**alfa + 1/(way**betta))/summ

        penny = rnd.choices([0, 1], [1-probability, probability])

        return penny

    for i in range(N):

        actual_point = int(start_point)
        n = int(n_towns)

        route_list = [actual_point]
        sum_kil = 0

        while (n-1) > 0:

            j = rnd.randint(0, n_towns-1)
            way = way_matrix[actual_point][j]
            t_way = ti[actual_point][j]
            wway = way_matrix[actual_point]
            tt = ti[actual_point]

            if way !=0 and j not in route_list:
                if __is__(way, t_way, list(wway), tt, alfa, betta):
                    actual_point = j
                    route_list.append(j)
                    sum_kil += way
                    n -= 1


        if way_matrix[start_point][route_list[-1]] != 0 :
            for i in route_list:
                delta_ti[i][i-1] += n_towns/sum_kil


    print(delta_ti)

    for i in range(n_towns):
        for j in range(n_towns):
            ti[i][j] = ti[i][j] * k + delta_ti[i][j]


    return ti

for i in range(3):
    print(colony(way_matrix))

