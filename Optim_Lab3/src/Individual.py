import random as rnd

class Individual:
    def __init__(self, gene_len, gene_number):
        self.ind_gene_len = gene_len
        self.ind_gene = "".join([rnd.choice(gene_number) for i in range(self.ind_gene_len)])
        self.ind_degree = 0

    def set_gene(self, new_gene):
        self.ind_gene = "".join(new_gene)
        assert type(self.ind_gene) == str, "Несовпадение типов"
