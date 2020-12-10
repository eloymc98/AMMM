'''
AMMM Lab Heuristics
GRASP solver
Copyright 2018 Luis Velasco.

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

import random
import copy
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha):

        # sort candidate assignments by highestLoad in ascending order
        sortedCandidateList = sorted(candidateList, key=lambda x: x.cost, reverse=False)

        # compute boundary highest load as a function of the minimum and maximum highest loads and the alpha parameter
        minHLoad = sortedCandidateList[0].cost
        maxHLoad = sortedCandidateList[-1].cost
        boundaryHLoad = minHLoad + (maxHLoad - minHLoad) * alpha

        # find elements that fall into the RCL
        maxIndex = 0
        for candidate in sortedCandidateList:
            if candidate.cost <= boundaryHLoad:
                maxIndex += 1

        # create RCL and pick an element randomly
        rcl = sortedCandidateList[0:maxIndex]  # pick first maxIndex elements starting from element 0
        if not rcl: return None
        return random.choice(rcl)  # pick a candidate from rcl at random

    def _greedyRandomizedConstruction(self, alpha):
        solution = self.instance.createSolution()
        assignment = 0
        complete = False
        while not complete:

            candidateList = solution.findFeasibleAssignments()

            # no candidate assignments => no feasible assignment found
            if not candidateList:
                solution.makeInfeasible()
                break

            candidate = self._selectCandidate(candidateList, alpha)

            pc_or_sc = 'primary' if candidate.is_primary is True else 'secondary'
            solution.assign(candidate.city, candidate.location,
                            candidate.type, pc_or_sc, check_completeness=True)
            complete = solution.complete
            assignment += 1

        return solution

    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        incumbent.makeInfeasible()
        incumbent.cost = float('infinity')
        cost = incumbent.cost
        self.writeLogLine(cost, 0)

        iteration = 0
        while not self.stopCriteria():
            iteration += 1

            # force first iteration as a Greedy execution (alpha == 0)
            # alpha = 0 if iteration == 1 else self.config.alpha
            alpha = self.config.alpha
            solution = self._greedyRandomizedConstruction(alpha)
            if self.config.localSearch:
                localSearch = LocalSearch(self.config, None)
                endTime = self.startTime + self.config.maxExecTime
                solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            if solution.isFeasible():
                solutionLowestCost = solution.cost
                if solutionLowestCost < cost:
                    incumbent = copy.deepcopy(solution)
                    cost = solutionLowestCost
                    self.writeLogLine(cost, iteration)

        self.writeLogLine(cost, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent
