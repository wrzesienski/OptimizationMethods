import random as rnd
import numpy as np
from Optim_Lab2.src.Plotting import *

N = 15  # количество муравьев в популяции
start_point = 1  # вершина начала маршрута
feromone_on_road = 400

def calc_delta_EAC(graph_matrix, ti, alpha, betta, sigma=0):
    """ рассчитывает приращение значения феромонов на
    пройденных муравьями маршрутах за один цикл"""

    node_number = len(graph_matrix[0])  # количество вершин графа

    delta_ti = [[0 for i in range(node_number)] for j in range(node_number)]  # матрица приращения
    actual_best_route = []
    actual_best_way = np.math.inf

    def sort_ways(s_route, s_way):
        """ возвращает список потенциальных вершин, к которым
        муравей может перебраться на данной итерации, т.е:
        - функция отсекает те вершины, в которых муравей уже был
        - функция отсекает вершины, с которыми у муравья нет связи"""
        return [i for i in range(len(s_way)) if s_way[i] > 0 and i not in s_route]

    def calc_sum(point, sort):

        node_ways = [graph_matrix[point][i] for i in sorted(sort)]
        node_ti = [ti[point][i] for i in sorted(sort)]

        summary = 0
        for i in range(len(node_ways)):
            summary += node_ti[i] ** alpha + 1 / (node_ways[i] ** betta)

        return summary

    def __is_chosen_way__(this_way, this_t, local_summ):
        """ возвращает значение True или False в зависимости от выпадения
        монетки """

        # вероятность перехода по маршруту
        probability = (this_t ** alpha + 1 / (this_way ** betta)) / local_summ
        # произойдет переход или нет
        penny = rnd.choices([0, 1], [1 - probability, probability])

        return penny

    for i in range(N):

        # вершина, в которой находится муравей/ сколько городов осталось пройти
        actual_stop, n_left = start_point, (node_number - 1)

        route_list = [actual_stop]
        way_length = 0  # суммарная длина маршрута

        while n_left > 0:

            potential_ways = list(graph_matrix[actual_stop])

            # отсортированный список возможных вершин, к которым может добраться муравей
            sort_route_pointer = sort_ways(route_list, potential_ways)

            # print(sort_route_pointer)

            if not len(sort_route_pointer): break  # муравей зашел в тупик на последней итерации

            "минус данного алгоритма: необходимо учесть добавление в \
            суммарную длину маршрута того расстояния, которое пройдет муравей \
            по возвращении в начальный город. Учитывается ниже"
            if len(sort_route_pointer) and n_left == 1:
                way_length += graph_matrix[sort_route_pointer[0]][start_point]

            # в случайном порядке выбираем потенциальное ребро
            next_stop = rnd.choice(sort_route_pointer)
            # берем значение его длины:
            way = graph_matrix[actual_stop][next_stop]

            # берем величину феромона ребра:
            t_way = ti[actual_stop][next_stop]

            way_X_pheromone = calc_sum(actual_stop, sort_route_pointer)

            if __is_chosen_way__(way, t_way, way_X_pheromone):
                actual_stop = next_stop  # муравей переходит в новую вершину
                route_list.append(next_stop)  # добавление в маршрутный лист
                way_length += way
                n_left -= 1

        else:
            " главное отличие элитной колонии: перезапись лучшего пути"
            if way_length <= actual_best_way: # перезапись лучшего результата
                actual_best_way = int(way_length)
                actual_best_route = list(route_list)

    for num in range(node_number):
        j, k = sorted((actual_best_route[num], actual_best_route[num - 1]))
        delta_ti[j][k] += feromone_on_road / actual_best_way  # заполнение матрицы выше главной диагонали

    return delta_ti


def calc_ti_elit(ti, delta_ti, p):
    """ рассчитывает новое значение феромонов ребер графа"""

    node_number = len(ti[0])
    t_min = 2
    t_max = 8

    for i in range(node_number):
        for j in range(i, node_number):
            ti[i][j] = ti[j][i] = ti[i][j] * p + delta_ti[i][j]

            # контроль феромонов на пути
            if ti[i][j] <= t_min: ti[i][j] = ti[j][i] = int(t_min)
            elif ti[i][j] >= t_max: ti[i][j] = ti[j][i] = int(t_max)

    return






