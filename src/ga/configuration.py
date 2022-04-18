import numpy as np


class MSimConfiguration:
    def __init__(self):
        self.perceptrons = 2 ** np.random.randint(1, 13)
        self.history_length = np.random.randint(1, 33)
        self.weight_bits = np.random.randint(1, 33)

        self.decode_width = 2 ** np.random.randint(1, 6)
        self.issue_width = 2 ** np.random.randint(1, 6)
        self.commit_width = 2 ** np.random.randint(1, 6)

        self.rob_size = 2 ** np.random.randint(5, 11)
        self.iq_size = 2 ** np.random.randint(5, 11)

        self.ialu = np.random.randint(2, 9)
        self.fpalu = np.random.randint(2, 9)
        self.imult = np.random.randint(1, 9)
        self.fpmult = np.random.randint(1, 9)

        x = np.random.randint(3, 8)
        y = np.random.randint(3, 8)

        self.dl1_sets = 2 ** np.random.randint(1, 16)
        self.dl1_block_size = 2**x
        self.dl1_assoc = 2 ** np.random.randint(0, 4)
        self.dl1_replacement_strat = np.random.choice(["l", "r", "f"])

        self.il1_sets = 2 ** np.random.randint(1, 16)
        self.il1_block_size = 2**y
        self.il1_assoc = 2 ** np.random.randint(0, 4)
        self.il1_replacement_strat = np.random.choice(["l", "r", "f"])

        self.ul2_sets = 2 ** np.random.randint(8, 19)
        self.ul2_block_size = 2 ** np.random.randint(
            max(x, y) + 1 if max(x, y) > 6 else 6, 9
        )
        self.ul2_assoc = 2 ** np.random.randint(1, 5)
        self.ul2_replacement_strat = np.random.choice(["l", "r", "f"])

        if self.ul2_sets * self.ul2_block_size < self.il1_sets * self.il1_block_size:
            self.ul2_sets, self.il1_sets = self.il1_sets, self.ul2_sets
        elif self.ul2_sets * self.ul2_block_size < self.dl1_sets * self.dl1_block_size:
            self.ul2_sets, self.dl1_sets = self.dl1_sets, self.ul2_sets

        dl1_size = self.dl1_block_size * self.dl1_sets
        il1_size = self.il1_block_size * self.il1_sets
        ul2_size = self.ul2_block_size * self.ul2_sets

    def get_clargs(self):
        cache_dl1 = f"-cache:dl1 dl1:{self.dl1_sets}:{self.dl1_block_size}:{self.dl1_assoc}:{self.dl1_replacement_strat} "
        cache_il1 = f"-cache:il1 il1:{self.il1_sets}:{self.il1_block_size}:{self.il1_assoc}:{self.il1_replacement_strat} "
        cache_ul2 = f"-cache:il2 dl2 -cache:dl2 ul2:{self.ul2_sets}:{self.ul2_block_size}:{self.ul2_assoc}:{self.ul2_replacement_strat} "
        other_config = f"-bpred perceptron -bpred:perceptron {self.perceptrons} {self.weight_bits} {self.history_length} -issue:width {self.issue_width} -commit:width {self.commit_width} -decode:width {self.decode_width} -rob:size {self.rob_size} -iq:size {self.iq_size} -res:ialu {self.ialu} -res:imult {self.imult} -res:fpalu {self.fpalu} -res:fpmult {self.fpmult} "

        return (other_config + cache_dl1 + cache_il1 + cache_ul2).split()
