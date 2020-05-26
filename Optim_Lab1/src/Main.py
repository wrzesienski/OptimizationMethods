import random as rnd
import math
import time
from colorama import *
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt


class Function:
    """ Класс функции """

    def __init__(self):
        self.x = rnd.uniform(-16, 16)
        self.y = rnd.uniform(-16, 16)
        self.z = Function.calc_func(self)
        # self.z = math.inf

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_z(self, z):
        self.z = z

    def set_all(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_any_pams(self, pam: str):
        """
        возвращает актуальные x, y, z:
        - "z" : z
        - "x" : x
        - "y" : y
        - "xyz" : x,y,z
        :return: выбранную величину
        """
        case_switcher = {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'xyz': [self.x, self.y, self.z]
        }
        return case_switcher[pam]

    def calc_func(self):
        """ вычисление значения функции заданного класса функции"""
        return (-10 / (0.005 * (self.x ** 2 + self.y ** 2)
                       - math.cos(self.x) * math.cos(self.y / np.sqrt(2)) + 2) + 10)


class Comtrade:
    """ класс массива, записывающего маршрут координат поиска экстремум"""

    def __init__(self):
        self.x_mass = []
        self.y_mass = []
        self.z_mass = []

    def append_to_mass(self, x, y, z):
        self.x_mass.append(x)
        self.y_mass.append(y)
        self.z_mass.append(z)

    def get_any_pams(self, pam: str):
        """
        возвращает актуальные x, y, z:
        - "z" : z_mass
        - "x" : x_mass
        - "y" : y_mass
        :return: выбранную величину
        """
        case_switcher = {
            'x': self.x_mass,
            'y': self.y_mass,
            'z': self.z_mass,
            'xyz': [self.x_mass, self.y_mass, self.z_mass]
        }
        return case_switcher[pam]

    def clear_all(self):
        """ подчищает списки в случае неудовлетворительной попытки"""
        self.x_mass.clear()
        self.y_mass.clear()
        self.z_mass.clear()


def do_anneal(function_body: Function, comtrade_list: Comtrade,
              t_init, t_min, step, accuracy, num="1"):
    """   МЕТОД ИМИТАЦИИ ОТЖИГА

    :param function_body: тело функции
    :param comtrade_list: тело комтрейда
    :param t_init: начальная температура
    :param t_min: минимальная температура
    :param step: шаг
    :param accuracy: точность
    :return: запись с маршрутом алгоритма
    """

    def temp_behaviour(temp, t_init, sume):

        """ возвращает новое значение температуры в зависимости от
        применяемого подхода
        :param temp: температура на итерации
        :param t_init: начальная температура
        :param sume: сумма
        :return: новое значение температуры
        """

        caser = {
            '1': t_init / math.log1p(sume),  # Больцмановский отжиг
            '2': t_init / (1 + sum),  # Отжиг Коши
            '3': temp * 0.95,  # Закон Коши
        }
        return caser[num]

    def get_new_random():
        """ возвращает случайное значение"""
        return rnd.uniform(-16, 16)

    def __is_less_1__(prob):
        """ если вероятность меньше 1, то True
            в противном случае - False """
        if prob <= 1: return 1
        return 0

    temp = t_init  # температура на первой итерации

    sum = 0  # параметр суммы

    while True:

        x, y, z = function_body.get_any_pams(pam="xyz")

        # логика выхода/рестарта алгоритма
        if temp <= t_min:  # условие остывания
            if z <= accuracy:  # условие заданной точности
                print(Fore.GREEN, "extrem is found")
                time.sleep(2)
                break
            else:  # выполнение алгоритма заново
                print(Fore.RED, "didnt get an extem, cycle it again")
                time.sleep(2)
                comtrade_list.clear_all()  # перезапись комтрейд
                temp = t_init
                sum = 0

        new_z = function_body.calc_func()  # новое значение функции

        probability = math.exp(-(new_z - z) / temp)  # вероятность перехода
        if not __is_less_1__(probability): probability = 1  # если z_new < z, то переход состоится точно

        # print(Fore.WHITE, "x: %f, y: %f, z: %f," % (x, y, new_z))
        # print(Fore.WHITE, "temperature: %f and probability: %f" % (temp, probability))

        penny = rnd.choices([0, 1], [1 - probability, probability])[0]  # псевдослучайное подбрасывание монеты

        if new_z < z or penny:  # если новое значение функции ниже, либо рандом хочет, чтобы переход состоялся
            function_body.set_z(z=new_z)
            comtrade_list.append_to_mass(x, y, new_z)  # запись
            # print(Fore.GREEN, "new x: %f, new y: %f, new z: %f," % (x, y, new_z))

        # новые случайные значения
        function_body.set_x(get_new_random())
        function_body.set_y(get_new_random())

        sum += step
        temp = temp_behaviour(temp, t_init, sum)  # понижение температуры

    return comtrade_list


def do_gradient_descend(function_body: Function, comtrade_list: Comtrade,
                        delta_x, delta_y, accuracy, step):
    """  МЕТОД ГРАДИЕНТНОГО СПУСКА

    :param function_body: тело функции
    :param comtrade_list: тело комтрейда
    :param delta_x: дельта х
    :param delta_y: дельта y
    :param accuracy: точность
    :param step: шаг
    :return: запись маршрута алгоритма
    """

    initial_step = int(step)

    def get_twins_delta_func(x, y, choice: str):

        f = Function()

        if choice == "grad_zx":
            f.set_x(x + delta_x)
            f.set_y(y)
        elif choice == "grad_zy":
            f.set_x(x)
            f.set_y(y + delta_y)

        return f, f.calc_func()

    loc_func_extrem = Function()
    counter = 0
    mean = accuracy  # mean - значение условия выхода из алгоритма

    while mean >= accuracy:
        x, y, z = function_body.get_any_pams(pam="xyz")
        comtrade_list.append_to_mass(x, y, z)  # запись комтрейд

        # получаем временный объект класса Function и новое значение функции
        f_zx, new_zx = get_twins_delta_func(x, y, "grad_zx")
        f_zy, new_zy = get_twins_delta_func(x, y, "grad_zy")

        z_list = [function_body, f_zx, f_zy] # список из функций

        counter += 1

        if counter % 20 == 0: # откат в наилучшее записанное состояние
            function_body.set_x(loc_func_extrem.get_any_pams("x"))
            function_body.set_y(loc_func_extrem.get_any_pams("y"))
            function_body.set_z(loc_func_extrem.calc_func())
            # print("new local pams:" , function_body.get_any_pams("xyz"))
            continue

        for i in range(len(z_list)):
            zz = z_list[i].calc_func()
            loc_extrem = loc_func_extrem.calc_func()

            # если экстремума объекта функции ниже экстремума лучшего экземпляра функции то происходит перезапись
            # лучшей функции
            if zz < loc_extrem:

                loc_func_extrem.set_x(z_list[i].get_any_pams("x"))
                loc_func_extrem.set_y(z_list[i].get_any_pams("y"))

        # print(loc_extrem, function_body.calc_func(), f_zx.calc_func(), f_zy.calc_func())

        # расчет градиентов по осям координат
        grad_zx = (new_zx - z) / delta_x
        grad_zy = (new_zy - z) / delta_y

        mean = math.sqrt((grad_zx) ** 2 + (grad_zy) ** 2) # актуальное приближение по точности

        print("grad x: %f, grad y: %f" % (grad_zx, grad_zy))
        print("mean: %f" % mean)
        print("step i: %f" % step)

        step = step / (1.01 + 0.001 * counter)  # дробим шаг и избегаем ситуации бесконченого зацикления
        if step < accuracy: step = int(initial_step/2)

        # новый конечный шаг
        step_x = -step * grad_zx
        step_y = -step * grad_zy

        # значение величин на следующей итерации
        # if throw_penny(): x += step_x
        # elif throw_penny(): y += step_y
        # else:
        x += step_x
        y += step_y

        # задаем новые свойства объекта функции
        function_body.set_x(x)
        function_body.set_y(y)
        function_body.set_z(function_body.calc_func())

        comtrade_list.append_to_mass(x, y, z)  # запись комтрейд
        time.sleep(2)

    print("extrem is found")

    return comtrade_list


def plot_route(comtrade):
    xx, yy, zz = comtrade.get_any_pams("xyz")
    # Plots GD

    x_gd = [xx[i] for i in range(1, len(xx))]
    y_gd = [yy[i] for i in range(1, len(xx))]

    N = 200

    xgd = np.linspace(-16, 16, N)
    ygd = np.linspace(-16, 16, N)

    X_gd, Y_gd = np.meshgrid(xgd, ygd)

    funcy = Function()
    Z_gd = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            funcy.set_x(xgd[i])
            funcy.set_y(ygd[j])
            Z_gd[i, j] = funcy.calc_func()

    Z_gd = Z_gd.transpose()

    fontsize1 = 15

    fig = plt.figure()
    fig.suptitle("Alforithm route", fontsize=fontsize1)
    fig.set_figheight(15)
    fig.set_figwidth(15)

    plt.contourf(X_gd, Y_gd, Z_gd, 100)
    plt.colorbar()

    plt.plot([x_gd[i] for i in range(len(x_gd))], [y_gd[i] for i in range(len(x_gd))], 'mo-')

    plt.plot(-0.00, -0.00, 'ro')
    plt.plot(x_gd[0], y_gd[0], "go")
    plt.plot(xx[-1], yy[-1], "ko")
    plt.text(-0.00015,
             0.00015,
             "(0,0)", color="k")

    plt.xlabel('$x$', fontsize=fontsize1)
    plt.ylabel('$y$', fontsize=fontsize1)

    plt.show()
    return


def do_scatter(comtrade):
    xx, yy, zz = comtrade.get_any_pams("xyz")

    xs = np.arange(-20, 20, 0.1)
    ys = np.arange(-20, 20, 0.1)

    def XYZcreator(xs, ys):
        X, Y = np.meshgrid(xs, ys)
        Z = (-10 / (0.005 * (X ** 2 + Y ** 2) - np.cos(X) * np.cos(Y / np.sqrt(2)) + 2) + 10)
        if (xs.shape == (1,) and ys.shape == (1,)):
            return Z[0]
        else:
            return X, Y, Z

    X, Y, Z = XYZcreator(xs, ys)

    surface = go.Surface(
        opacity=0.75,
        x=X,
        y=Y,
        z=Z,
    )
    # Блок для точки
    dot = go.Scatter3d(
        x=xx,
        y=yy,
        z=zz,
        mode='markers',
        marker=dict(
            size=3,
            line=dict(
                color='rgb(111, 203, 1)',
                width=0.5)
        )
    )
    data = [surface, dot]
    layout = go.Layout(title='My func and dot', autosize=False,
                       width=500, height=500,
                       margin=dict(l=65, r=50, b=65, t=90))

    fig = go.Figure(data=data, layout=layout)

    fig.show()

    return


# comtrade_anneal = do_anneal(Function(), Comtrade(),
#                             t_init=5, t_min=0.5, step=5, accuracy=0.5)
# x, y, z = comtrade_anneal.get_any_pams("xyz")
# num_extrem = z.index(min(z))
# print(" Final point: f(%f,%f) = %f" % (x[num_extrem],y[num_extrem],min(z)))
#
# plot_route(comtrade_anneal)
# # do_scatter(comtrade_anneal)




comtrade_gradient = do_gradient_descend(Function(), Comtrade(),
                                        delta_x=0.4, delta_y=0.4, accuracy=0.0001, step=5)

plot_route(comtrade_gradient)
# do_scatter(comtrade_gradient)

x, y, z = comtrade_gradient.get_any_pams("xyz")
print(" Final point: f(%f,%f) = %f" % (x[-1], y[-1], z[-1]))
