from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from configuration import MSimConfiguration
import sys
import subprocess


class MSimProblem(FloatProblem):
    def __init__(self, benchmark_path):
        super(MSimProblem, self).__init__()

        self.number_of_objectives = 2
        self.number_of_constraints = 0
        self.number_of_variables = 24

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ["Energy", "CPI"]

        self.benchmark_path = benchmark_path
        self.file_counter = 1

        self.lower_bound = [
            2,
            1,
            1,
            2,
            2,
            2,
            32,
            32,
            2,
            2,
            1,
            1,
            2,
            8,
            1,
            0,
            2,
            8,
            1,
            0,
            256,
            64,
            2,
            0,
        ]

        self.upper_bound = [
            4096,
            32,
            32,
            32,
            32,
            32,
            1024,
            1024,
            8,
            8,
            8,
            8,
            32768,
            256,
            8,
            2,
            32768,
            256,
            8,
            2,
            2097152,
            256,
            16,
            2,
        ]

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        config = MSimConfiguration()

        args = (
            [
                "./sim-outorder",
                "-redir:sim",
                f"results/sim_config_{self.file_counter}.res",
                "-redir:prog",
                "results/out.prg",
                "-max:inst",
                "1000000",
            ]
            + config.get_clargs()
            + [self.benchmark_path]
        )

        print(f"Running simulator for config {self.file_counter}")

        # Open sim-outorder process with args
        process = subprocess.run(args, check=False, stdout=subprocess.DEVNULL)

        # Get IPC and power from file
        energy = self.__get_attribute_from_file(
            f"results/sim_config_{self.file_counter}.res", "Total Power Consumption"
        )

        cpi = 1 / self.__get_attribute_from_file(
            f"results/sim_config_{self.file_counter}.res", "THROUGHPUT IPC"
        )

        solution.objectives[0] = energy
        solution.objectives[1] = cpi

        print(f"Sim_{self.file_counter}: Energy: {energy} CPI: {cpi}")

        self.file_counter += 1

        return solution

    def __get_attribute_from_file(self, file, attribute):
        with open(file) as fp:
            for line in fp:
                if line.startswith(attribute):
                    return float(line.split(":")[1].strip())

    def get_name(self):
        return "MSim simple perceptron problem"
