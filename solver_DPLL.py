import numpy as np
import copy
import time
# import sys
# sys.setrecursionlimit(10000)

LEN = 20
STOP = False
START = 0

class Instance:
    def __init__(self, arr):
        self.array = arr # np.array(arr, dtype=int)
        self.fixed = np.full(LEN, fill_value=False)
        self.values = np.full(LEN, fill_value=False)

    def find_unfixed(self):
        for i in range(len(self.fixed)):
            if not self.fixed[i]:
                return i

    def fix_value(self, i, b):
        """
        Will fix i-th variable on b
        """
        # print(f"\tFixing value {i} to {b}")
        self.fixed[i] = True
        self.values[i] = b

    def pure_variable(self):
        """
        Check pure variables and set thems
        """
        for i in range(LEN):
            if (self.fixed[i] == False):
                if self.is_in(i+1):
                    if not self.is_in(-i-1):
                        self.fix_value(i, True)
                elif self.is_in(-i-1):
                        self.fix_value(i, False)
                # delete occurrence if fixed

    def is_in(self, literal):
        for clause in self.array:
            if literal in clause:
                return True
        return False

    def fix_one_value_clause(self):
        """
        If there are one literal clauses they will be set
        """
        changed = False
        # arr = self.array.copy() # need copy?
        for literal in self.array:
            if (len(literal) == 1):
                self.fix_value(abs(literal[0])-1, (literal[0] > 0))
                self.remove_variable(literal[0])
                changed = True
                break
        # self.array = arr
        if (changed):
            self.fix_one_value_clause()

    def remove_variable(self, var):
        for x in self.array:
            if (var in x ):
                self.array.remove(x)
                if (len(self.array) == 0):
                    print('NOT SAT')
                    STOP = True
            if (-var in x ):
                x.remove(-var)
                if (len(x) == 0):
                    print('NOT SAT')
                    STOP = True

    def is_satisfiable(self):
        if (len(self.array) == 0):
            return
        for clause in self.array:
            clauses = []
            for literal in clause:
                # take negation of values
                clauses.append(not self.values[abs(literal)-1] if literal > 0 else self.values[abs(literal)-1])
            if (all(clauses)):
                return
        duration = time.time() - START
        print(f"Found in time: {duration}")
        print(f"Solveable for: {np.array(self.values, dtype=np.uint8)}")
        global STOP
        STOP = True

class DPLL_SAT_solver:
    """
    This class solves SAT problems
    """

    def __init__(self, file):
        arr = []
        while (1):
            line = next(file)
            splited_line = line.split()
            if (splited_line[0] != 'c'):
                global LEN
                LEN = int(splited_line[2])
                break
        while (1):
            line = next(file)
            splited_line = line.split()
            if (splited_line[0] == '%'):
                break
            arr.append([int(x) for x in splited_line[:-1]])
        
        global START
        START = time.time()
        self.solve_DPLL(Instance(arr))

    def solve_DPLL(self, problem):
        problem.pure_variable()
        problem.fix_one_value_clause()
        problem.is_satisfiable()
        if STOP:
            return
        self.fix_one_value(problem)

    def fix_one_value(self, problem):
        unfixed = problem.find_unfixed()
        if unfixed is not None:
            problem2 = copy.deepcopy(problem)

            problem.fix_value(unfixed, True)
            self.solve_DPLL(problem)

            problem2.fix_value(unfixed, False)
            self.solve_DPLL(problem2)

