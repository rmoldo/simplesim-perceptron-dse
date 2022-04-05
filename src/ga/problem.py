from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution


class MSimProblem(FloatProblem):
    def __init__(self):
        self.number_of_objectives = 2
        self.number_of_constraints = 0
        self.number_of_variables = 4  # TODO: add real number of variables when ready

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ["Energy", "CPI"]

        self.lower_bound = []
        self.upper_bound = []

        super(MSimProblem, self).__init__()
        pass

    def evaluate(self, solution: FloatSolution) -> FloatSolution:

        return solution

    def get_name(self):
        return "MSim simple perceptron problem"
