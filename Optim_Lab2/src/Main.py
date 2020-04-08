# import numpy as np
from Optim_Lab2.src.StandartAntColony import *

class Comtrade:
    """ класс записи результатов"""

    def __init__(self):
        self.alfa = []
        self.betta = []
        self.p = []
        self.time = []
        self.shortest_way = []

    def set_coefficients(self, alfa, betta, p):
        self.alfa.append(alfa)
        self.betta.append(betta)
        self.p.append(p)

    def get_coefficients(self):
        return self.alfa, self.betta, self.p

    def record_results(self, time, way_length):
        self.time.append(time)
        self.shortest_way.append(way_length)

    def show_results(self):
        return self.time, self.shortest_way

# матрица ребер графов
way_matrix = np.load("C:/Users/Alexander/PythonProjects/"
                     "OptimizationMethods/Optim_Lab2/data/Task3.npy")

"(4,10), (10,1), (1,9), (9,5), (5,3), (3,2), (2,6), (6,7), (7,8), (8,4), "
" 120 "
print("матрица путей: \n", way_matrix)

# создание двухмерного списка феромонов
ti = [[0 for i in range(len(way_matrix[0]))] for j in range(len(way_matrix[0]))]

print("time: ", stopwatch(way_matrix, ti, 0.95, 1, 1))


# my_comtrade = Comtrade()
#
# a_b = [(i+1)/10 for i in range(0, 101, 20)]
# p_list = [i/10 for i in range(0, 11, 2)]
# counter = 0
# for a in a_b:
#     for b in a_b:
#         for p in p_list:
#             my_comtrade.set_coefficients(a, b, p)
#
#             time = stopwatch(way_matrix, ti, p, a, b)
#             way = calc_shortest_way(way_matrix, ti)
#             my_comtrade.record_results(time, way)
#             counter += 1
#             print(counter)
#
#
# print(my_comtrade.time)
