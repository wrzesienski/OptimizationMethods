import time
from Optim_Lab2.src.Plotting import *
from Optim_Lab2.src.AntColony import *
from Optim_Lab2.src.ClassicAntAlgorithm import *
from Optim_Lab2.src.EliteAntColony import *
import numpy as np


def calc_most_way(way_matrix, ti):
    """расчет прогнозируемого кратчайшего пути
     по актуальной матрице феромонов
    :param way_matrix: матрица путей
    :param ti: матрица феромонов
    :return: кратчайший путь
    """

    node_number = len(ti[0])  # разряд матрицы

    init_mean = goal_mean = summary = 0  # точка итерации/точка-цель/общий путь

    shortest_way = [int(init_mean)]  # матрица кратчайшего пути
    for i in range(node_number - 1):

        local_max = 0
        for j in range(node_number):
            if ti[init_mean][j] > local_max and j not in shortest_way:
                goal_mean = j
                local_max = ti[init_mean][j]
        shortest_way.append(goal_mean)
        summary += way_matrix[init_mean][goal_mean]
        init_mean = int(goal_mean)

    summary += way_matrix[shortest_way[0]][shortest_way[-1]]  # учет возврата в первый город

    # print("кратчайший путь на данный момент: ", shortest_way, " и его длина: ", summary)

    return summary


def stopwatch(way_matrix, ti, p, alfa, betta, sigma=0, algorithm=1):
    """
    секундомер выполнения алгоритма с указанными параметрами
    :param way_matrix: матрица путей графа
    :param ti: матрица феромонов путей графа
    :param p: коэффициент p
    :param alfa: коэффициент alpha
    :param betta: коэффициент betta
    :param sigma: коэффициент sigma
    :param algorithm: выбранн
    :return: время выполнения алгоритма
    """

    p5 = 150  # необходимое условие вхождения в погрещность
    delta_ti = []
    # создадим словари для универсального переключения функций алгоритмов
    calc_delta = {'CAA': calc_delta_CAA, 'AC': calc_delta_AC, 'EAC': calc_delta_EAC}
    calc_increment = {'CAA': calc_ti, 'AC': calc_ti, 'EAC': calc_ti_elit}

    start_data = time.perf_counter()  # начало отсчета времени выполнения алгоритма

    while calc_most_way(way_matrix, ti) > p5:

        # расчет нового значения матрицы феромонов
        delta_ti = calc_delta[algorithm](way_matrix, ti, alfa, betta, sigma)
        calc_increment[algorithm](ti, delta_ti, p)

        # принудительно завершаем деффективные итерации
        if time.perf_counter() - start_data >= 15.0:
            return -1

    return round(time.perf_counter() - start_data, 4)


def analize(way_graph, algorithm, is_sigma=False):
    """
    функция анализа времени выполнения алгоритма путем перебора всех
    входящих в него коэффициентов
    :param way_graph: матрица путей графа
    :param algorithm: анализируемый алгоритм
    :param is_sigma: перебор сигмы
    :return:
    """
    alpha_beta = [(i + 1) / 10 for i in range(0, 101, 50)]
    p_list = [i / 10 for i in range(0, 11, 5)]
    counter = 0
    sigma = 0.5

    my_comtrade = Comtrade()

    for a in alpha_beta:
        for b in alpha_beta:
            for p in p_list:
                my_comtrade.set_coefficients(a, b, p)

                ti = [[5 for i in range(len(way_graph[0]))] for j in range(len(way_graph[0]))]

                if is_sigma: p, sigma = sigma, p

                my_time = stopwatch(way_graph, ti, p, a, b, sigma, algorithm)
                way = calc_most_way(way_graph, ti)
                if my_time == -1:  # отсекаем долгое прохождение по алгоритму
                    my_comtrade.record_results(0, 150)
                else:  # качественный алгоритм
                    my_comtrade.record_results(my_time, way)

                counter += 1
                print("alpha: %f, beta: %f, p: %f, time: %f, length: %d" % (a, b, p, my_time, way))

    to_plot(my_comtrade)


# матрица ребер графов
way_graph = np.load("C:/Users/Alexander/PythonProjects/"
                    "OptimizationMethods/Optim_Lab2/data/Task3.npy")

""" 
[[  0  25  63  60  97  37  46  76   2   0]
 [ 25   0   8 100  72   3  11  34  84  87]
 [ 63   8   0  75  17  38  75  93  50  66]
 [ 60 100  75   0  61  87  98  22  71   9]
 [ 97  72  17  61   0  24   1  44  14  83]
 [ 37   3  38  87  24   0  38  83  46  10]
 [ 46  11  75  98   1  38   0   7  73  28]
 [ 76  34  93  22  44  83   7   0  12  84]
 [  2  84  50  71  14  46  73  12   0  30]
 [  0  87  66   9  83  10  28  84  30   0]]"""

"(3,9), (9,0), (0,8), (8,4), (4,2), (2,1), (1,5), (5,6), (6,7), (7,3), "
" 120 "
print("матрица путей: \n", way_graph)

# создание двухмерного списка феромонов
# ti = [[10 for i in range(len(way_graph[0]))] for j in range(len(way_graph[0]))]
# #
# print("time: ", stopwatch(way_graph, ti, 0, 1, 1))


analize(way_graph, 'EAC')
