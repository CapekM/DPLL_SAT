import numpy as np
import copy
import time
# import sys
# sys.setrecursionlimit(10000)

LEN = 20
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

    def fix_value(self, i, b, name):
        """
        Will fix i-th variable on b
        """
        # print(f"\tFixing value {i} to {b}")
        # print(f"{name}: {len(self.array)}")
        self.fixed[i] = True
        self.values[i] = b
        i += 1
        if not b:
            i *= -1
        for_removal = []
        for clause in self.array:
            if (i in clause):
                # print(f"\t{clause} => []")
                for_removal.append(clause)
            if (-i in clause):
                y = clause.copy()
                clause.remove(-i)
                # print(f"\t{y} => {clause}")
                if (len(clause) == 0):
                    # print(f"\tN: {np.array(self.fixed, dtype=np.uint8)}")
                    return True
        self.array = [e for e in self.array if e not in for_removal]
        if (len(self.array) == 0):
            duration = time.time() - START
            print(f"\tIs SAT!")
            print(f"\t- Formula:\t{np.array(self.values, dtype=np.uint8)}")
            print(f"\t- Time: \t{duration}")
            exit(0)
        return False

    # def fix_value(self, i, b, name):
    #     """
    #     Will fix i-th variable on b
    #     """
    #     self.fixed[i] = True
    #     self.values[i] = b
    #     i += 1
    #     if not b:
    #         i *= -1
    #     for x in self.array:
    #         if (i in x ):
    #             self.array.remove(x)
    #             if (len(self.array) == 0):
    #                 duration = time.time() - START
    #                 print(f"Found in time: {duration}")
    #                 print(f"SAT for: {np.array(self.values, dtype=np.uint8)}")
    #                 exit(0)
    #         if (-i in x ):
    #             x.remove(-i)
    #             if (len(x) == 0):
    #                 return True
    #     return False

    def pure_variable(self):
        """
        Check pure variables and set thems
        """
        for i in range(LEN):
            if (self.fixed[i] == False):
                if self.is_in(i+1):
                    if not self.is_in(-i-1):
                        return self.fix_value(i, True, "pure_variable")
                elif self.is_in(-i-1):
                        return self.fix_value(i, False, "pure_variable")

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
                return self.fix_value(abs(literal[0])-1, (literal[0] > 0), "fix_one_value_clause")
                changed = True
                break
        # self.array = arr
        if (changed):
            self.fix_one_value_clause()

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
        duration = time.time() - START
        print("\tNot SAT!")
        print(f"\t- Time: {duration}")

    def solve_DPLL(self, problem):
        if problem.pure_variable():
            return
        if problem.fix_one_value_clause():
            return
        self.fix_one_value(problem)

    def fix_one_value(self, problem):
        unfixed = problem.find_unfixed()
        if unfixed is not None:
            length = len(problem.array)
            problem0 = copy.deepcopy(problem)
            problem1 = copy.deepcopy(problem)

            if (not problem0.fix_value(unfixed, True, "DPLL T")):
                # print("\tfirst")
                # print(f"\t{np.array(problem.fixed, dtype=np.uint8)}")
                # print(f"\t{np.array(problem0.fixed, dtype=np.uint8)}")
                self.solve_DPLL(problem0)

            if (not problem1.fix_value(unfixed, False, "DPLL F")):
                # print("\tsecond")
                # print(f"\t{np.array(problem.fixed, dtype=np.uint8)}")
                # print(f"\t{np.array(problem1.fixed, dtype=np.uint8)}")
                self.solve_DPLL(problem1)
