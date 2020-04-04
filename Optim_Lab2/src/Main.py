# import numpy as np
from Optim_Lab2.src.StandartAntColony import *


# матрица ребер графов
way_matrix = np.load("C:/Users/Alexander/PythonProjects/"
                     "OptimizationMethods/Optim_Lab2/data/Task3.npy")

"(4,10), (10,1), (1,9), (9,5), (5,3), (3,2), (2,6), (6,7), (7,8), (8,4), "
" 120 "
print("матрица путей: \n", way_matrix)

# создание двумерного списка феромонов
ti = [[0 for i in range(len(way_matrix[0]))] for j in range(len(way_matrix[0]))]







print("time: " ,stopwatch(way_matrix, ti, 0.95, 1, 1))