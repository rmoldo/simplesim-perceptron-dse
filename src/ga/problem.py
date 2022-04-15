from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from configuration import MSimConfiguration
import sys
import subprocess


class MSimProblem(FloatProblem):
    def __init__(self, benchmark):
        super(MSimProblem, self).__init__()

        self.number_of_objectives = 2
        self.number_of_constraints = 0
        self.number_of_variables = 4  # TODO: add real number of variables when ready

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ["Energy", "CPI"]

        self.benchmark = benchmark
        self.file_counter = 1

        self.lower_bound = []
        self.upper_bound = []

        pass

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        config = MSimConfiguration()

        args = (
            [
                "./sim-outorder",
                "-redir:sim",
                f"results/sim_config_{self.file_counter}.res",
                "-max:inst",
                "1000000",
            ]
            + config.get_clargs()
            + [self.benchmark]
        )

        # Open sim-outorder process with args
        process = subprocess.run(args, check=False, stdout=subprocess.DEVNULL)

        # Get IPC and power from file
        energy = self.__get_attribute_from_file("Total Power Consumption")
        cpi = 1 / self.__get_attribute_from_file("THROUGHPUT IPC")

        solution.objectives[0] = energy
        solution.objectives[1] = cpi

        return solution

    def __get_attribute_from_file(self, attribute):
        pass

    def get_name(self):
        return "MSim simple perceptron problem"
