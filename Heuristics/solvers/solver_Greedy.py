"""
AMMM Project
Greedy solver
Eloy Marín, Pablo Pazos
File given Luis Velasco and under its copyright policy
Modified for project purposes
"""

import random, time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_Greedy(_Solver):

    def _selectCandidate(self, candidateList):
        if self.config.solver == 'Greedy':
            # sort candidate assignments by cost in ascending order
            sortedCandidateList = sorted(candidateList, key=lambda x: x.cost)
            # choose assignment with minimum cost
            best_candidates = []
            min_value = sortedCandidateList[0].cost
            for c in sortedCandidateList:
                if c.cost == min_value:
                    best_candidates.append(c)
                else:
                    break
            # if there are multiple assignments with min cost, select one randomly
            return random.choice(best_candidates)
        return random.choice(candidateList)

    def construction(self):
        # get an empty solution for the problem
        solution = self.instance.createSolution()
        assignment = 0
        complete = False
        while not complete:

            # get feasible assignments
            candidates = solution.findFeasibleAssignments()

            # no candidate assignments => no feasible assignment found
            if not candidates:
                print('Greedy construction is infeasible. Please try again!')
                solution.makeInfeasible()
                break

            # assign the assignment with min cost
            candidate_with_min_cost = self._selectCandidate(candidates)

            pc_or_sc = 'primary' if candidate_with_min_cost.is_primary is True else 'secondary'
            solution.assign(candidate_with_min_cost.city, candidate_with_min_cost.location,
                            candidate_with_min_cost.type, pc_or_sc, check_completeness=True)
            # print(f'City {candidate_with_min_cost.city.getId()}, Location {candidate_with_min_cost.location.getId()},
            # Type {candidate_with_min_cost.type.get_id()}, Cost {solution.cost}, {pc_or_sc}')
            complete = solution.complete
            assignment += 1

        return solution

    def solve(self, **kwargs):
        self.startTimeMeasure()

        solver = kwargs.get('solver', None)
        if solver is not None:
            self.config.solver = solver

        localSearch = kwargs.get('localSearch', None)
        if localSearch is not None:
            self.config.localSearch = localSearch

        self.writeLogLine(float('inf'), 0)

        solution = self.construction()
        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.cost, 1)
        self.numSolutionsConstructed = 1
        if self.config.localSearch:
            localSearch = LocalSearch(self.config, None)
            endTime = self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.printPerformance()

        return solution
