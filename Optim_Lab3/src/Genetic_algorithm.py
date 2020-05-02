import math
from colorama import Style

from Optim_Lab3.src.Individual import *

def make_genetic_algorithm(gene, gene_number):
    """
    генетический алгоритм оптимизации
    :param gene:
    :return:
    """

    GENE_LIST = list(gene)  # разбивка строки на символьный список
    GENE_LEN = len(GENE_LIST) # длина генома
    POP_LEN = 900  # размер популяции

    pop1 = [Individual(GENE_LEN, gene_number) for i in range(POP_LEN)]  # создание новой популяции
    pop2 = [Individual(GENE_LEN, gene_number) for i in range(POP_LEN)]  # создание новой популяции
    generation = 1

    def make_evaluation(population):
        """
        проводит оценку особей популяции.
        :param population: оцениваемая популяция
        :return: лучшая особь
        """

        master_individ = Individual(GENE_LEN, gene_number)
        for i in range(POP_LEN):
            ind_list = list(population[i].ind_gene)
            degree = 1

            for j in range(GENE_LEN):
                degree += 1 if GENE_LIST[j] == ind_list[j] else 0

            population[i].ind_degree = degree
            master_individ = population[i] if degree > master_individ.ind_degree else master_individ

        return master_individ


    def get_selection(population):
        """
        проведение селекции лучших особей методом рулетки
        :return:
        """

        # делим популяцию поровну на готовых к селекции и нет
        best_individs = []

        if generation % 20 == 0:
            while len(best_individs) < 0.4 * POP_LEN:  # пока списки популяций не сравняются
                act_pop_len = len(population)

                # выбор особи на селекцию
                shot = rnd.choices([i for i in range(act_pop_len)],
                                   [population[i].ind_degree for i in range(act_pop_len)])[0]
                best_individs.append(population.pop(shot))  # добавление в список селекции

                # # турнир
                # pretendents = [rnd.randint(0, act_pop_len-1) for i in range(1, 3)]
                # winner = rnd.choices(pretendents, [population[i].ind_degree for i in pretendents])[0]
                #
                # best_individs.append(population.pop(winner))  # добавление в список селекции
        else:
                # селекция усечением
            population = sorted(population, key=(lambda ind: ind.ind_degree))
            best_individs = population[int(len(population) * 0.6):]
            population = population[:int(len(population) * 0.6)]


        return best_individs, population
        # return sorted(best_individs, key=(lambda ind: ind.ind_degree)), population

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

        parents = [parent_1, parent_2]

        # # скрещивание генов родителей
        son.ind_gene = "".join([rnd.choices(parents, [1, rnd.uniform(1.1,3)])[0][i] for i in range(GENE_LEN)])
        daughter.ind_gene = "".join([rnd.choices(parents, [1, rnd.uniform(1.1,3)])[0][i] for i in range(GENE_LEN)])

        # recessive_gene = parents[0]
        # dominant_gene = parents[1]
        # # создание 2 - точечного кроссовера
        # border1 = rnd.randint(0, int(GENE_LEN//2))
        #
        # son.ind_gene = "".join(recessive_gene[:border1] +
        #        dominant_gene[border1:])
        # daughter.ind_gene =  "".join(dominant_gene[:(GENE_LEN-border1)] +
        #        recessive_gene[(GENE_LEN-border1):])


        return son, daughter

    def crossbreed_individs(best_individs):
        """
        скрещивание особей
        :param best_individs:
        :return:
        """
        new_individs = []
        ind_len = len(best_individs)

        while len(new_individs) < ind_len:
            par_ind = [rnd.randint(0, len(best_individs) - 1), rnd.randint(0, len(best_individs) - 1)]
            degrees_list = sorted([best_individs[par_ind[0]], best_individs[par_ind[1]]], key= lambda ind: ind.ind_degree)
            parents_list = [list(degrees_list[0].ind_gene), list(degrees_list[1].ind_gene)]

            coincidence = 0
            for i in range(GENE_LEN):
                coincidence += 1 if parents_list[0][i] == parents_list[1][i] == gene[i] else 0

            # если есть оригинальные совпадения с заданным словом
            if math.fabs(degrees_list[0].ind_degree - coincidence) >= 1:
                new_individs.extend(cabbage_growing(parents_list[0], parents_list[1]))
                best_individs = [best_individs[i] for i in range(len(best_individs)) if i not in par_ind]
            # исключение участников


        return new_individs

    def mutate_individs(feeble_individs, master_degree):
        """
        процесс мутации
        :param feeble_individs:
        :return:
        """
        mutation_prob = 3 * math.log(master_degree) / GENE_LEN

        for i in range(len(feeble_individs)):
            individ_gene = list(feeble_individs[i].ind_gene)

            for j in range(GENE_LEN):
                if rnd.choices([0, 1], [1 - mutation_prob, mutation_prob])[0]:
                    individ_gene[j] = rnd.choice(gene_number)

            feeble_individs[i].ind_gene = "".join(individ_gene)

        return


    # init_plot(make_evaluation(pop1).ind_gene)

    while True:
        era = generation // 20
        print( "\nERA:", era, "GENERATION: ", generation % 20)

        master1= make_evaluation(pop1)

        master_list = list(master1.ind_gene)
        print("".join(["\033[34m{}".format(master_list[i]) if master_list[i] == GENE_LIST[i]
                       else "\033[31m{}".format(master_list[i]) for i in range(GENE_LEN)]),
                        Style.RESET_ALL, master1.ind_degree)

        master_board = list(master_list)

        if master1.ind_degree > GENE_LEN: break

        best_individs1, feeble_individs1 = get_selection(pop1)
        # print([best_individs1[i].ind_degree for i in range(len(best_individs1))])

        new_individs1 = crossbreed_individs(best_individs1)

        mutate_individs(feeble_individs1, master1.ind_degree)

        pop1 = new_individs1 + feeble_individs1

        master2= make_evaluation(pop2)
        best_individs2, feeble_individs2 = get_selection(pop2)
        new_individs2 = crossbreed_individs(best_individs2)
        mutate_individs(feeble_individs2, master2.ind_degree)
        pop2 = new_individs2 + feeble_individs2

        generation += 1
        if generation % 10 == 0:
            print("НОВАЯ ЭРА")
            # generation = 1
            pop1 = pop1[::2] + pop2[::2]
            pop2 = pop1[1::2] + pop2[1::2]

