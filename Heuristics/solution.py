"""
AMMM Lab Heuristics
Base representation of a solution instance
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
"""

from AMMMGlobals import AMMMException


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class _Solution(object):
    def __init__(self):
        self.fitness = 0.0
        self.feasible = True
        self.verbose = False

    def setVerbose(self, verbose):
        if not isinstance(verbose, bool) or (verbose not in [True, False]):
            raise AMMMException('verbose(%s) has to be a boolean value.' % str(verbose))
        self.verbose = verbose

    def getFitness(self):
        return self.fitness

    def makeInfeasible(self):
        self.feasible = False
        self.fitness = float('inf')

    def isFeasible(self):
        return self.feasible

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
