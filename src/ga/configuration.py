import numpy as np


class MSimConfiguration:
    def __init__(self):
        self.decode_width = 2 ** np.random.randint(1, 6)
        self.issue_width = 2 ** np.random.randint(1, 6)
        self.commit_width = 2 ** np.random.randint(1, 6)

        self.rob_size = 2 ** np.random.randint(5, 11)
        self.rb_size = 2 ** np.random.randint(5, 11)
        self.iq_size = 2 ** np.random.randint(5, 11)

        self.ialu = np.random.randint(2, 9)
        self.fpalu = np.random.randint(2, 9)
        self.imult = np.random.randint(1, 9)
        self.fpmult = np.random.randint(1, 9)

        self.dl1_sets = 2 ** np.random.randint(1, 16)
        self.dl1_block_size = 2 ** np.random.randint(3, 9)
        self.dl1_assoc = 2 ** np.random.randint(0, 4)
        self.dl1_replacement_strat = np.random.choice(["l", "r", "f"])

        self.il1_sets = 2 ** np.random.randint(1, 16)
        self.il1_block_size = 2 ** np.random.randint(3, 9)
        self.il1_assoc = 2 ** np.random.randint(0, 4)
        self.il1_replacement_strat = np.random.choice(["l", "r", "f"])

        self.ul2_sets = 2 ** np.random.randint(8, 22)
        self.ul2_block_size = 2 ** np.random.randint(6, 9)
        self.ul2_assoc = 2 ** np.random.randint(1, 5)
        self.ul2_replacement_strat = np.random.choice(["l", "r", "f"])

        dl1_size = self.dl1_block_size * self.dl1_sets
        il1_size = self.il1_block_size * self.il1_sets
        ul2_size = self.ul2_block_size * self.ul2_sets

        if dl1_size > ul2_size or il1_size > ul2_size:
            if dl1_size > il1_size:
                self.ul2_block_size, self.ul2_sets = self.dl1_block_size, self.dl1_sets
            else:
                self.ul2_block_size, self.ul2_sets = self.il1_block_size, self.il1_sets

    def get_clargs(self):
        # TODO: add perceptron config when ready
        cache_dl1 = f"-cache:dl1 dl1:{self.dl1_sets}:{self.dl1_block_size}:{self.dl1_assoc}:{self.dl1_replacement_strat} "
        cache_il1 = f"-cache:il1 il1:{self.il1_sets}:{self.il1_block_size}:{self.il1_assoc}:{self.il1_replacement_strat} "
        cache_ul2 = f"-cache:dl2 ul2:{self.ul2_sets}:{self.ul2_block_size}:{self.ul2_assoc}:{self.ul2_replacement_strat} "
        other_config = f"-issue:width {self.issue_width} -commit:width {self.commit_width} -decode:width {self.decode_width} -rob:size {self.rob_size} -rb:size {self.rb_size} -iq:size {self.iq_size} -res:ialu {self.ialu} -res:imult {self.imult} -res:fpalu {self.fpalu} -res:fpmult {self.fpmult} "

        return (other_config + cache_dl1 + cache_il1 + cache_ul2).split()
