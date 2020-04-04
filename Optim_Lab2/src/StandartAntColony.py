import time
import random as rnd
import numpy as np

N = 100  # количество муравьев в популяции
start_point = 0  # вершина начала маршрута


def calc_delta(graph_matrix, ti, alfa, betta):
    """ рассчитывает приращение количества феромонов на
    пройденных муравьями маршрутах"""

    node_number = len(graph_matrix[0])  # количество узлов графа

    delta_ti = [[0 for i in range(node_number)] for j in range(node_number)]  # приращение

    def calc_sum(wway, tt, alfa, betta):

        summ = 0

        for i in wway:
            if i == 0: wway.remove(0)

        for i in range(len(wway)):
            summ += tt[i] ** alfa + 1 / (wway[i] ** betta)

        return summ

    def __is_this_way__(this_way, this_t, local_summ, alfa, betta):
        """ возвращает значение True или False в зависимости от выпадения
        монетки """

        # вероятность перехода по маршруту
        probability = (this_t ** alfa + 1 / (this_way ** betta)) / local_summ

        # произойдет переход или нет
        penny = rnd.choices([0, 1], [1 - probability, probability])

        return penny

    for i in range(N):

        # вершина, в которой находится муравей/ сколько городов осталось пройти
        actual_point, n = start_point, (node_number - 1)

        route_list = [actual_point]
        way_length = 0  # суммарная длина маршрута

        while n > 0:  #

            # в случайном порядке выбираем потенциальное ребро
            j = rnd.randint(0, node_number - 1)
            # берем значение его длины:
            way = graph_matrix[actual_point][j]

            " FIXXXXXXX - возможность бесконечного зацикления!!!!!!!!!!!!!"
            if way != 0 and j not in route_list:  # если связь есть и через вершину еще не проходили

                # берем величину феромона ребра:
                t_way = ti[actual_point][j]
                rel_way_list = list(graph_matrix[actual_point])  # длины всех вершин, к которым можно добраться отсюда
                rel_ferom_list = list(ti[actual_point])  # феромоны всех вершин, к которым можно добраться

                way_on_pheromone = calc_sum(rel_way_list, rel_ferom_list, alfa, betta)

                if __is_this_way__(way, t_way, way_on_pheromone, alfa, betta):
                    actual_point = j  # муравей переходит в новую вершину
                    route_list.append(j)  # добавление в маршрутный лист
                    way_length += way
                    n -= 1
        # print("\n маршрут \n", route_list)

        if graph_matrix[start_point][route_list[-1]] != 0:  # связь последней вершиной с первой есть
            for i in range(len(route_list)):
                yes = route_list[i]
                before = route_list[i - 1]
                if yes < before:  # заполняем матрицу выше главной диагонали
                    delta_ti[yes][before] += node_number / way_length
                else:
                    delta_ti[before][yes] += node_number / way_length
        # print("\n матрица приращения: \n", delta_ti)

    return delta_ti


def calc_ti(ti, delta_ti, p):
    """ рассчитывает новое значение феромонов ребер графа"""

    node_number = len(ti[0])

    for i in range(node_number):
        for j in range(node_number):
            ti[i][j] = ti[j][i] = ti[i][j] * p + delta_ti[i][j]

    return ti


def calc_shortest_way(way_matrix, ti):
    """расчет кратчайшего пути по актуальной матрице феромонов
    :param way_matrix: матрица путей
    :param ti: матрица феромонов
    :return: кратчайший путь
    """

    node_number = len(ti[0])

    "FIXXXXX"
    init_mean = goal_mean = summary = 0
    # goal_mean = 0
    # suum = 0
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

    print("кратчайший путь на данный момент: ", shortest_way)

    return summary


def stopwatch(way_matrix, ti, p, alfa, betta):
    """ секундомер выполнения алгоритма с указанными параметрами"""

    pp = 200  # необходимое условие вхождения в погрещность

    start_data = time.perf_counter()  # начало отсчета времени выполнения алгоритма
    short = np.math.inf  # начальное значение кратчайшего пути

    while short > pp:
        # print("матрица феромонов :", ti)
        delta_ti = calc_delta(way_matrix, ti, alfa, betta)
        # print("\n матрица феромонов \n", ti)

        # расчет нового значения матрицы феромонов
        ti = calc_ti(ti, delta_ti, p)
        # расчет кратчайшего пути по доминантным феромонам
        short = calc_shortest_way(way_matrix, ti)

        print("\n итерация закончена")
        print("кратчайший путь:", short)

    return time.perf_counter() - start_data
