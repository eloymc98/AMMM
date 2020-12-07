'''
AMMM Lab Heuristics
Greedy solver
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import random, time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_Greedy(_Solver):

    def _selectCandidate(self, candidateList):
        if self.config.solver == 'Greedy':
            # sort candidate assignments by highestLoad in ascending order
            sortedCandidateList = sorted(candidateList, key=lambda x: x.highestLoad)
            # choose assignment with minimum highest load
            return sortedCandidateList[0]
        return random.choice(candidateList)

    def construction(self):
        # get an empty solution for the problem
        solution = self.instance.createSolution()

        assignments = 0
        while assignments < len(solution.cities) * 2:
            # get best assignment (cheapest one)
            candidate_with_min_cost = solution.findBestFeasibleAssignment()

            # no candidate assignments => no feasible assignment found
            if not candidate_with_min_cost:
                solution.makeInfeasible()
                break

            # assign the current task to the CPU that resulted in a minimum highest load

            pc_or_sc = 'primary' if candidate_with_min_cost.is_primary is True else 'secondary'
            solution.assign(candidate_with_min_cost.city, candidate_with_min_cost.location,
                            candidate_with_min_cost.type, pc_or_sc)
            assignments += 1

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
        self.writeLogLine(solution.getFitness(), 1)
        self.numSolutionsConstructed = 1
        if self.config.localSearch:
            localSearch = LocalSearch(self.config, None)
            endTime = self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.printPerformance()

        return solution
