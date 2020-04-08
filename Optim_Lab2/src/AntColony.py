import random as rnd
import numpy as np
from Optim_Lab2.src.Plotting import *

N = 20  # количество муравьев в популяции
start_point = 1  # вершина начала маршрута


def calc_delta(graph_matrix, ti, alfa, betta):
    """ рассчитывает приращение значения феромонов на
    пройденных муравьями маршрутах за один цикл"""

    node_number = len(graph_matrix[0])  # количество вершин графа

    global_delta_ti = [[0 for i in range(node_number)] for j in range(node_number)]  # матрица приращения

    actual_best_route = []
    actual_best_way = np.math.inf
    feromone_on_road = 10

    def sort_ways(s_route, s_way):
        """ возвращает список потенциальных вершин, к которым
        муравей может перебраться на данной итерации, т.е:
        - функция отсекает те вершины, в которых муравей уже был
        - функция отсекает вершины, с которыми у муравья нет связи"""
        return [i for i in range(len(s_way)) if s_way[i] > 0 and i not in s_route]

    def way_list(point, sort):
        """ возвращает список с длиной маршрутов, к которым муравей
        может добраться из данной вершины"""
        return [graph_matrix[point][i] for i in sorted(sort) if i > 0]

    def ti_list(point, tii):
        """ возвращает список со значением феромонов маршрутов,
        к которым муравей может добраться из данной вершины"""
        return [ti[point][i] for i in sorted(tii) if i > 0]

    def compare(a, b):
        """сравнивает и возвращает числа в порядке возрастания"""
        if a < b:
            return a, b
        return b, a

    def calc_sum(wway, tt):

        summary = 0
        for i in range(len(wway)):
            summary += tt[i] ** alfa + 1 / (wway[i] ** betta)

        return summary

    def __is_chosen_way__(this_way, this_t, local_summ):
        """ возвращает значение True или False в зависимости от выпадения
        монетки """

        # вероятность перехода по маршруту
        probability = (this_t ** alfa + 1 / (this_way ** betta)) / local_summ
        print("вероятность ", probability)
        # произойдет переход или нет
        penny = rnd.choices([0, 1], [1 - probability, probability])

        return penny


    for i in range(N):

        delta_ti = [[0 for i in range(node_number)] for j in range(node_number)]  # матрица приращения

        # вершина, в которой находится муравей/ сколько городов осталось пройти
        actual_stop, n_left = start_point, (node_number - 1)

        route_list = [actual_stop]
        way_length = 0  # суммарная длина маршрута

        while n_left > 0:

            potential_ways = list(graph_matrix[actual_stop])

            # отсортированный список возможных вершин, к которым может добраться муравей
            sort_route_pointer = sort_ways(route_list, potential_ways)

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

            way_on_pheromone = calc_sum(
                                        way_list(actual_stop, sort_route_pointer),  # лист длин путей к соседям
                                        ti_list(actual_stop, sort_route_pointer))  # лист феромонов на соседних путях

            if __is_chosen_way__(way, t_way, way_on_pheromone):
                actual_stop = next_stop  # муравей переходит в новую вершину
                route_list.append(next_stop)  # добавление в маршрутный лист
                way_length += way
                n_left -= 1

        else:  # выполняется в случае успешного достижения начальной точки
            for num in range(node_number):
                j, k = compare(route_list[num], route_list[num - 1])
                delta_ti[j][k] += node_number / way_length  # заполнение матрицы выше главной диагонали

            calc_ti(ti,delta_ti, 0.99)

        if way_length <= actual_best_way:  # перезапись лучшего результата

            actual_best_way = int(way_length)
            actual_best_route = list(route_list)

    for num in range(node_number):
        j, k = compare(actual_best_route[num], actual_best_route[num - 1])
        global_delta_ti[j][k] += feromone_on_road / actual_best_way  # заполнение матрицы выше главной диагонали

    print("\n маршрут \n", actual_best_route)
    print("\n матрица приращения: \n", delta_ti)

    return global_delta_ti


def calc_ti(ti, delta_ti, p):
    """ рассчитывает новое значение феромонов ребер графа"""

    node_number = len(ti[0])

    for i in range(node_number):
        for j in range(node_number):
            ti[i][j] = ti[j][i] = ti[i][j] * p + delta_ti[i][j]

    return


def calc_shortest_way(way_matrix, ti):
    """расчет прогнозируемого кратчайшего пути
     по актуальной матрице феромонов
    :param way_matrix: матрица путей
    :param ti: матрица феромонов
    :return: кратчайший путь
    """

    node_number = len(ti[0])

    init_mean = goal_mean = summary = 0

    shortest_way = [int(init_mean)]
    for i in range(node_number - 1):

        local_max = 0
        for j in range(node_number):
            if ti[init_mean][j] > local_max and j not in shortest_way:
                goal_mean = j
                local_max = ti[init_mean][j]
        shortest_way.append(goal_mean)
        summary += way_matrix[init_mean][goal_mean]
        init_mean = int(goal_mean)

    summary += way_matrix[shortest_way[0]][shortest_way[-1]] # учет возврата в первый город

    # print("кратчайший путь на данный момент: ", shortest_way)

    # build_a_route(shortest_way)

    return summary