import math
from colorama import Style

from src.Individual import *

GENE_LIST = GENE_LEN = POP_LEN = 0
gene = gene_number = ""


def make_genetic_algorithm(gene, gene_number):
    """
    генетический алгоритм оптимизации
    :param gene: идеальный геном
    :param gene_number: возможная выборка генов
    :return:
    """

    def make_evaluation(population):
        """
        проводит оценку особей популяции.
        :param population: оцениваемая популяция
        :return: лучшая особь
        """

        master_individ = Individual(GENE_LEN, gene_number)  # создание экземпляра доминантного индивида

        for i in range(POP_LEN):
            ind_list = list(population[i].ind_gene)
            degree = 1

            for j in range(GENE_LEN):  # оценка схожести с идеалом
                degree += 1 if GENE_LIST[j] == ind_list[j] else 0

            population[i].ind_degree = degree  # присвоение оценки

            # перезапись доминанта при совпадении условий
            master_individ = population[i] if degree > master_individ.ind_degree else master_individ

        return master_individ

    def get_selection(population):
        """
        проведение селекции лучших особей методом рулетки
        :return:
        """

        # делим популяцию поровну на готовых к селекции и нет
        best_individs = []
        if rnd.randint(0,1):  # селекция рулеткой
            while len(best_individs) < 0.3 * POP_LEN:
                act_pop_len = len(population)

                # псевдослучайный выбор особи на скрещивание
                # winner = rnd.choices([i for i in range(act_pop_len)],
                #                    [population[i].ind_degree/act_pop_len for i in
                #                     range(act_pop_len)])[0]
                # winner = rnd.choices([i for i in range(act_pop_len)],
                #                    [population[i].ind_degree/math.log(math.e + (population[i].ind_degree)) for i in range(act_pop_len)])[0]
                #
                # турнир
                pretendents = [rnd.randint(0, act_pop_len - 1) for i in range(1, 5)]
                winner = rnd.choices(pretendents, [population[i].ind_degree for i in pretendents])[0]

                best_individs.append(population.pop(winner))  # добавление в список селекции

        else:  # селекция усечением

            # сортировка популяции по оценкам и срез
            population = sorted(population, key=(lambda ind: ind.ind_degree))
            best_individs = population[int(len(population) * 0.7):]
            population = population[:int(len(population) * 0.7)]

        return best_individs, population

    def cabbage_growing(parent_1, parent_2):
        """
        скрещивание 2х особей
        :param parent_1: родитель1
        :param parent_2: родитель2
        :return: 2 потомка особей
        """

        # создание экземляров потомков
        son = Individual(GENE_LEN, gene_number)
        daughter = Individual(GENE_LEN, gene_number)
        if rnd.randint(0,1):  # псевдоравномерное скрещивание

            daughter.ind_gene = "".join(parent_2)
            son.ind_gene = "".join([rnd.choices([parent_1, parent_2], [1, 1])[0][i] for i in range(GENE_LEN)])

        else:  # создание 1 - точечного кроссовера

            border1 = rnd.randint(0, int(GENE_LEN // 2))
            #
            son.ind_gene = "".join(parent_1[:border1] + parent_2[border1:])
            daughter.ind_gene =  "".join(parent_2[:(GENE_LEN-border1)] + parent_1[(GENE_LEN-border1):])

        return son, daughter

    def crossbreed_individs(best_individs):
        """
        скрещивание особей
        :param best_individs: выборка особей на скрещивание
        :return: скрещенная популяция
        """
        new_individs = []
        ind_len = len(best_individs)

        while len(new_individs) < ind_len:

            # случайный выбор партнеров на скрешивание
            par_ind = [rnd.randint(0, len(best_individs) - 1), rnd.randint(0, len(best_individs) - 1)]

            # составление рабочих списков из выбранных особей
            degrees_list = sorted([best_individs[par_ind[0]], best_individs[par_ind[1]]],
                                  key=lambda ind: ind.ind_degree)
            parents_list = [list(degrees_list[0].ind_gene), list(degrees_list[1].ind_gene)]

            coincidence = 0  # совпадение по генам
            for i in range(GENE_LEN):
                coincidence += 1 if parents_list[0][i] == parents_list[1][i] == gene[i] else 0

            " если худшая особь имеет некоторое количество оригинальных хороших" \
            "генов, то пара скрещивается"
            if math.fabs(degrees_list[0].ind_degree - coincidence) >= 1:
                # скрещивание и добавление потомков в новую популяцию
                new_individs.extend(cabbage_growing(parents_list[0], parents_list[1]))
                # сокращение списка потенциальных партнеров
                best_individs = [best_individs[i] for i in range(len(best_individs)) if i not in par_ind]

        return new_individs

    def mutate_individs(feeble_individs):
        """
        процесс мутации
        :param feeble_individs:
        :return:
        """

        mutation_prob = 1 / GENE_LEN

        for i in range(len(feeble_individs)):
            individ_gene = list(feeble_individs[i].ind_gene)

            for j in range(GENE_LEN):
                if rnd.choices([0, 1], [1 - mutation_prob, math.fabs(mutation_prob)])[0]:
                    individ_gene[j] = rnd.choice(gene_number)

            feeble_individs[i].ind_gene = "".join(individ_gene)

        return

    def output_inform(master):

        master_list = list(master.ind_gene)
        print("".join(["\033[34m{}".format(master_list[i]) if master_list[i] == GENE_LIST[i]
                       else "\033[31m{}".format(master_list[i]) for i in range(GENE_LEN)]),
              Style.RESET_ALL, master.ind_degree)

    def handle_genotype(pop):
        """
        обработка популяции
        :param pop: популяция
        :return: новая популяция
        """
        best_individs, feeble_individs = get_selection(pop)  # селекция
        # print([best_individs[i].ind_degree for i in range(len(best_individs))], len(best_individs))
        new_individs = crossbreed_individs(best_individs)  # скрещивание
        mutate_individs(feeble_individs)  # мутация

        return feeble_individs + new_individs  # новая популяция

    GENE_LIST = list(gene)  # разбивка строки на символьный список
    GENE_LEN = len(GENE_LIST)  # длина генома
    POP_LEN = 20
    # размер популяции
    STEP = 100  # шаг смены эры
    assert POP_LEN % 4 == 0, "Размер популяции приведет к зацикливанию"

    pop1 = [Individual(GENE_LEN, gene_number) for i in range(POP_LEN)]  # создание новой популяции
    # pop2 = [Individual(GENE_LEN, gene_number) for j in range(POP_LEN)]  # создание новой популяции
    # pop3 = [Individual(GENE_LEN, gene_number) for i in range(POP_LEN)]  # создание новой популяции
    generation = 1

    while True:


        print("\nERA:", generation // STEP, "GENERATION: ", generation % STEP)

        # оценка популяций
        master1 = make_evaluation(pop1)
        # master2 = make_evaluation(pop2)

        # master3 = make_evaluation(pop3)

        # вывод схожестей генов
        output_inform(master1)
        # output_inform(master2)
        # output_inform(master3)

        # условие выхода из алгоритма
        # if (master1.ind_degree > GENE_LEN) or (master2.ind_degree > GENE_LEN)\
        #         or (master3.ind_degree > GENE_LEN): break
        # if (master1.ind_degree > GENE_LEN) or (master2.ind_degree > GENE_LEN): break
        if (master1.ind_degree > GENE_LEN): break

        # проведение селекции, скрещивания и мутации
        pop1 = handle_genotype(pop1)
        # pop2 = handle_genotype(pop2)

        # pop3 = handle_genotype(pop3, master3.ind_degree)

        generation += 1
        # if generation % STEP == 0:
        #     print("НОВАЯ ЭРА: ПЕРЕМЕШИВАНИЕ ПЛЕМЕН")
        #     pop1 = pop1[::2] + pop2[::2]
            # pop1 = pop1[::3] + pop2[::3] + pop3[::3]
            # pop2 = pop1[1::2] + pop2[1::2]
            # pop2 = pop1[1::3] + pop2[1::3] + pop3[1::3]
            # pop3 = pop1[2::3] + pop2[2::3] + pop3[2::3]
