import numpy as np
import matplotlib.pyplot as plt

def build_a_route(way):

    X = [10, 10, 100, 100, 30, 20, 20, 50, 50, 85]
    Y = [5, 85, 0, 90, 50, 55, 50, 75, 25, 50]

    plt.title("Общий путь-", size=14)
    X1=[X[way[i]] for i in np.arange(0,10,1)]
    Y1=[Y[way[i]] for i in np.arange(0,10,1)]
    plt.plot(X1, Y1, color='r', linestyle=' ', marker='o')
    plt.plot(X1, Y1, color='b', linewidth=1)
    X2=[X[way[10-1]],X[way[0]]]
    Y2=[Y[way[10-1]],Y[way[0]]]
    plt.plot(X2, Y2, color='g', linewidth=2,  linestyle='-', label='Путь от  последнего n к первому городу')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()
