from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.problem import ZDT1
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions
from problem import MSimProblem
import argparse

if __name__ == "__main__":
    COMMAND_PARSER = argparse.ArgumentParser(
        description="DSE for m-sim with simple perceptron predictor"
    )

    COMMAND_PARSER.add_argument(
        "benchmark_path",
        metavar="benchmark_path",
        type=str,
        help="Benchmark file path",
    )

    COMMAND_PARSER.add_argument(
        "population_size",
        metavar="population_size",
        type=int,
        help="Population size: positive integer",
    )

    COMMAND_PARSER.add_argument(
        "offspring_population_size",
        metavar="offspring_population_size",
        type=int,
        help="Offspring population size: positive integer",
    )

    COMMAND_PARSER.add_argument(
        "max_eval",
        metavar="max_eval",
        type=int,
        help="Maximum evaluations: positive integer",
    )

    ARGS = COMMAND_PARSER.parse_args()

    benchmark_name = ARGS.benchmark_path.split("/")[-1].split(".")[0]

    problem = MSimProblem(ARGS.benchmark_path)

    algorithm = NSGAII(
        problem=problem,
        population_size=ARGS.population_size,
        offspring_population_size=ARGS.offspring_population_size,
        mutation=PolynomialMutation(
            probability=1.0 / problem.number_of_variables, distribution_index=20
        ),
        crossover=SBXCrossover(probability=1.0, distribution_index=20),
        termination_criterion=StoppingByEvaluations(ARGS.max_eval),
    )

    algorithm.run()
    solutions = algorithm.get_result()
    front = get_non_dominated_solutions(solutions)

    plot_front = Plot("Pareto front approximation", axis_labels=["Energy", "CPI"])
    plot_front.plot(
        front,
        label="NSGAII m-sim with perceptron predictor "
        + benchmark_name
        + f" max eval {ARGS.max_eval}",
        filename="DSE_for_" + benchmark_name + f"_max_eval_{ARGS.max_eval}",
        format="png",
    )
