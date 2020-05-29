def show_simplex_table(a, b, c, profit):
    """ функция вывода значений в виде симплекс таблицы"""
    elem_num = len(a[0])  # количество неизвестных

    el_list = ["x" + str(i + 1) for i in range(elem_num)] + ["у.е."]

    for j in range(len(el_list)):
        print("| %s " % el_list[j], end="   |")
    print("\n", "-- " * 20)
    for i in range(len(b)):
        for j in range(elem_num):
            print("| %.3f " % a[i][j], end="|")

        print("| %.3f |" % b[i])
        print("-- " * 20)

    for i in range(elem_num):
        print("| %.3f " % c[i], end="|")
    print("| %.3f |" % profit)


def get_canon_form(a, b, c):
    """функция приведения системы к каноническому виду"""

    for i in range(len(b)):
        a = [a[j] + [1] if i == j else a[j] + [0] for j in range(len(a))]
        c += [0]
    return a, c


def simplex_method():
    # вариант 3
    a1 = [12, 2, 4]  # расход ресурсов на продажу 1 вида товара
    a2 = [22, 12, 6]  # расход ресурсов на продажу 2 вида товара
    a3 = [3, 23, 9]  # расход ресурсов на продажу 3 вида товара
    a = [a1, a2, a3]

    b = [910, 755, 823]  # ограничение видов ресурсов
    c = [-1, -3, -7]  # прибыль от продажи каждой группы товара
    profit = 0  # прибыль

    a, c = get_canon_form(a, b, c)  # приводим к каноническому виду

    # пока есть отрицательные коэффициенты
    while [elem for elem in c if elem < 0]:

        print("\nЗАХОДИМ НА ИТЕРАЦИЮ\n")
        show_simplex_table(a, b, c, profit)
        row_num = c.index(min(c))  # индекс наименьшего отрицательного элемента
        print("\nНаименьший отрицательный элемент и его столбец: %.3f, %d" % (c[row_num], row_num))
        b_on_num = [b[i] / a[i][row_num] for i in range(len(b))]
        string_num = b_on_num.index(min(b_on_num))  # наименьший индекс расхода
        print("Выбранная строка и столбец: %d, %d \n" % (string_num + 1, row_num + 1))
        b[string_num] = b[string_num] / a[string_num][row_num]  # изменяем значение расхода
        print("\nПромежуточные изменения: разделили строку %d на %.3f\n"
              % (string_num+1, a[string_num][row_num]))
        a[string_num] = [el / a[string_num][row_num] for el in a[string_num]]  # делим все элементы на row_num элемент
        show_simplex_table(a, b, c, profit)

        for i in range(len(b)): # вычисляем у.е.
            if i == string_num: continue #flag
            b[i] -= b[string_num] * a[i][row_num]
        profit += b[string_num] * abs(c[row_num])

        print("\nПроизвели вычисления со столбцом у.е.\n")
        show_simplex_table(a, b, c, profit)

        for j in range(len(a[string_num])):  # почисленно по каждому элементу
            for i in range(len(a)):  # проходим по каждому уравнению а
                if i == string_num: continue  # flag
                # если элемент базового столбца больше нуля, то вычитаем, если нет, то прибавляем
                a[i][j] += -a[string_num][j] * a[i][row_num]
            c[j] += -a[string_num][j] * c[row_num]
            print("\nПроизвели вычисления со столбцом x%d\n" % (j+1))
            show_simplex_table(a, b, c, profit)

        print("\nИТОГ НА ИТЕРАЦИИ\n")
        show_simplex_table(a, b, c, profit)

    print("\nНаилучший путь составил: %.3f у.е." % profit)

    return


simplex_method()
