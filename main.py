import click
import numpy as np

from reference import Solver
from solver_DPLL import DPLL_SAT_solver

LEN = 20

class SAT_problem:
    def __init__(self, arr):
        self.array = arr # np.array(arr, dtype=int)
        self.fixed = np.full(LEN, fill_value=False)
        self.assigned = np.full(LEN, fill_value=False)
        self.values = np.full(LEN, fill_value=False)

class SAT_solver:
    """
    This class solves SAT problems
    """

    def __init__(self, file):
        arr = []
        while (1):
            line = next(file)
            splited_line = line.split()
            if (splited_line[0] != 'c'):
                LEN = splited_line[2]
                break
        while (1):
            line = next(file)
            splited_line = line.split()
            if (splited_line[0] == '%'):
                break
            arr.append([int(x) for x in splited_line[:-1]])
        self.problem = SAT_problem(arr)

    def unit_propagate(self, array):
        changed = False
        arr = array
        for literal in array:
            if (len(literal) == 1):
                self.fix_value(abs(literal[0])-1, (literal[0] > 0))
                for x in arr:
                    if (literal[0] in x ):
                        arr.remove(x)
                    if (-literal[0] in x ):
                        x.remove(-literal[0])
                        if (len(x) == 0):
                            self.stop = True
                        if (len(x) == 1):
                            changed = True
        if (changed):
            return self.unit_propagate(arr)
        return arr

    def pure_variable(self, array):
        for i in range(LEN):
            if (self.problem.fixed[i] == False):
                if self.is_in(i+1):
                    if not self.is_in(-i-1):
                        self.fix_value(i, True)
                elif self.is_in(-i-1):
                        self.fix_value(i, False)

    def fix_value(self, i, b):
        print(f"\tFixing value {i} to {b}")
        self.problem.fixed[i] = True
        self.problem.values[i] = b

    def is_in(self, literal):
        for clause in self.problem.array:
            if literal in clause:
                return True
        return False

    def solve_BT(self):
        self.problem.array = self.unit_propagate(self.problem.array)
        self.pure_variable(self.problem.array)
        # values = np.full(LEN, fill_value=False)
        self.stop = False
        self.solveable = False
        self.recursive_BT(self.problem.values, 0)

        if (self.solveable):
            print('Solveable')
        else:
            print('Not solveable')

    def recursive_BT(self, values, i):
        if (self.stop or i >= LEN):
            return
        if (self.is_satisfiable(values)):
            stop = True
            return
        if (self.problem.fixed[i]):
            self.recursive_BT(values, i+1)
        else:
            values[i] = False
            # print(f"- {np.array(values, dtype=np.uint8)}: {i}")
            self.recursive_BT(values, i+1)
            values[i] = True

            # print(f"+ {np.array(values, dtype=np.uint8)}: {i}")
            self.recursive_BT(values, i+1)

    def is_satisfiable(self, values):
        for clause in self.problem.array:
            clauses = []
            for literal in clause:
                # take negation of values
                clauses.append(not values[abs(literal)-1] if literal > 0 else values[abs(literal)-1])
            if (all(clauses)):
                return False
        print(f"Solveable for: {np.array(values, dtype=np.uint8)}")
        self.solveable = True
        return True

@click.command()
@click.option('-p', '--path', type=click.File('r'), default='uf20-91/uf20-01.cnf', # callback=get_token,
              help='File with problems.', required=True)
def hello(path):
    """tool for SAT"""
    # solver = SAT_solver(path)
    # solver.solve_BT()

    DPLL_SAT_solver(path)

    # s = Solver('uf20-91/uf20-02.cnf')
    # s.run()
    # print(f"XXX {s.compute_cnf()}")

if __name__ == '__main__':
    hello()
