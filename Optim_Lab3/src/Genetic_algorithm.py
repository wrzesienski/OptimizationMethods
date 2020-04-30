from Optim_Lab3.src.Individual import *

def make_genetic_algorithm(gene, gene_number):
    """
    генетический алгоритм оптимизации
    :param gene:
    :return:
    """

    GENE_LIST = list(gene)  # разбивка строки на символьный список
    GENE_LEN = len(GENE_LIST) # длина генома
    POP_LEN = 200  # размер популяции


    # actual_population = [Individual(GENE_LEN, gene_number) for i in range(POP_LEN)]  # создание новой популяции
    pop1 = [Individual(GENE_LEN, gene_number) for i in range(POP_LEN)]  # создание новой популяции
    pop2 = [Individual(GENE_LEN, gene_number) for i in range(POP_LEN)]  # создание новой популяции

    def make_evaluation(population):
        """
        проводит оценку особей популяции.
        :param population: оцениваемая популяция
        :return: лучшая особь
        """

        master_individ = Individual(GENE_LEN, gene_number)
        for i in range(POP_LEN):
            ind_list = list(population[i].ind_gene)
            degree = 0

            for j in range(GENE_LEN):
                degree += 1 if GENE_LIST[j] == ind_list[j] else 0

            population[i].ind_degree = degree
            master_individ = population[i] if degree > master_individ.ind_degree else master_individ

        print(master_individ.ind_gene, master_individ.ind_degree)
        return master_individ


    def get_selection(population):
        """
        проведение селекции лучших особей методом рулетки
        :return:
        """

        # делим популяцию поровну на готовых к селекции и нет
        best_individs = []

        # селекция усечением
        population = sorted(population, key=(lambda ind: ind.ind_degree))
        best_individs = population[int(len(population) * 0.7) + 1:]
        population = population[:int(len(population) * 0.7) + 1]

        # while len(best_individs) < len(population): # пока списки популяций не сравняются
        #     act_pop_len = len(population)

            # # выбор особи на селекцию
            # shot = rnd.choices([i for i in range(act_pop_len)],
            #                    [population[i].ind_degree**2/act_pop_len for i in range(act_pop_len)])[0]
            # best_individs.append(population.pop(shot))  # добавление в список селекции

            # # турнир
            # pretendents = [rnd.randint(int((i - 1)/3 * act_pop_len), int(i / 3 * act_pop_len)-1) for i in range(1, 4)]
            # winner = rnd.choices(pretendents, [population[i].ind_degree**2 for i in pretendents])[0]

            # best_individs.append(population.pop(winner))  # добавление в список селекции

        return best_individs, population

    def cabbage_growing(parent_1, parent_2):
        """
        скрещивание 2х особей
        :param parent_1: родитель1
        :param parent_2: родитель2
        :return: 2 потомка особей
        """

        parents = [mom_gene, dad_gene] = list(parent_1.ind_gene), list(parent_2.ind_gene)
        # parents = sorted([parent_1, parent_2], key=(lambda ind:ind.ind_degree))
        # recessive_gene = list(parents[0].ind_gene)
        # dominant_gene = list(parents[1].ind_gene)
        # domination = (parents[0].ind_degree / parents[1].ind_degree)
        # print(domination)

        # создание 2 - точечного кроссовера
        border1 = rnd.randint(0, len(mom_gene)//3)
        border2 = rnd.randint(border1, len(mom_gene)*2//3)


        # создание экземляров потомков
        son = Individual(GENE_LEN, gene_number)
        daughter = Individual(GENE_LEN, gene_number)

        # скрещивание генов родителей в случайном порядке

        son.ind_gene = "".join(rnd.choice(parents)[:border1] +
               rnd.choice(parents)[border1:border2] + rnd.choice(parents)[border2:])
        daughter.ind_gene =  "".join(rnd.choice(parents)[:border1] +
               rnd.choice(parents)[border1:border2] + rnd.choice(parents)[border2:])
        # son.ind_gene = "".join(recessive_gene[:int((1-(1+domination)/4)*len(recessive_gene))] +
        #        dominant_gene[int((1-(1+domination)/4)*len(recessive_gene)):])
        # daughter.ind_gene =  "".join(dominant_gene[:int((1+domination)/4*len(recessive_gene))] +
        #        recessive_gene[int((1+domination)/4*len(recessive_gene)):])


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

            new_individs.extend(cabbage_growing(
                                best_individs[par_ind[0]], best_individs[par_ind[1]]))

            # исключение участников
            best_individs = [best_individs[i] for i in range(len(best_individs)) if i not in par_ind]

        return new_individs

    def mutate_individs(feeble_individs):
        """
        процесс мутации
        :param feeble_individs:
        :return:
        """
        # mutation_prob = 1 / GENE_LEN

        for i in range(len(feeble_individs)):
            individ_gene = list(feeble_individs[i].ind_gene)
            mutation_prob = 1 / (1 + feeble_individs[i].ind_degree/2)
            for j in range(GENE_LEN):
                # if rnd.choices([0, 1],[mutation_prob, 1 - mutation_prob]):
                if rnd.choices([0, 1],[1 - mutation_prob, mutation_prob])[0]:
                    individ_gene[j] = rnd.choice(gene_number)

            feeble_individs[i].ind_gene = "".join(individ_gene)

        return

    generation = 1

    while True:

        master1 = make_evaluation(pop1)
        master2 = make_evaluation(pop2)
        if master1.ind_degree == GENE_LEN: break

        best_individs1, feeble_individs1= get_selection(pop1)
        best_individs2, feeble_individs2= get_selection(pop2)

        new_individs1 = crossbreed_individs(best_individs1)
        new_individs2 = crossbreed_individs(best_individs2)

        mutate_individs(feeble_individs1)
        mutate_individs(feeble_individs2)

        pop1 = new_individs1 + feeble_individs1
        pop2 = new_individs2 + feeble_individs2

        generation +=1
        if generation >=200:
            print("Создание нового поколения")
            generation = 1
            pop1 = ([Individual(GENE_LEN, gene_number) for i in range(POP_LEN-int(len(new_individs1)/2))]
                                + new_individs2[::4] + new_individs1[::4])
            pop2 = ([Individual(GENE_LEN, gene_number) for i in range(POP_LEN-int(len(new_individs1)/2))]
                                + new_individs2[::4] + new_individs1[::4])
