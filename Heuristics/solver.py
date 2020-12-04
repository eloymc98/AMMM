'''
AMMM Lab Heuristics
Abstract solver
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

import time
from Heuristics.logger import Logger


class _Solver(object):
    def __init__(self, config, instance):
        self.config = config
        self.instance = instance
        logFields = [
            {'id': 'elapTime', 'name': 'Elap. Time (s)', 'headerformat': '{:>14s}', 'valueformat': '{:>14.8f}'},
            {'id': 'objValue', 'name': 'Obj. Value', 'headerformat': '{:>10s}', 'valueformat': '{:>10.8f}'},
            {'id': 'iterations', 'name': 'Iterations', 'headerformat': '{:>12s}', 'valueformat': '{:>12d}'}
        ]
        self.logger = Logger(fields=logFields)
        if instance is not None and self.config.verbose:
            self.logger.printHeaders()
        self.startTime = 0
        self.elapsedEvalTime = 0
        self.numSolutionsConstructed = 0
    
    def startTimeMeasure(self):
        self.startTime = time.time()
    
    def writeLogLine(self, objValue, iterations):
        if not self.config.verbose: return
        logValues = {'elapTime': time.time() - self.startTime, 'objValue': objValue, 'iterations': iterations}
        self.logger.printValues(logValues)

    def solve(self, **kwargs):
        raise NotImplementedError('Abstract method cannot be called')

    def printPerformance(self):
        if not self.config.verbose: return
        avg_evalTimePerCandidate = 0.0
        if self.numSolutionsConstructed != 0:
            avg_evalTimePerCandidate = 1000.0 * self.elapsedEvalTime / float(self.numSolutionsConstructed)

        print('Evaluation Performance:')
        print('  Num. solutions constructed', self.numSolutionsConstructed)
        print('  Total Eval. Time     ', self.elapsedEvalTime, 's')
        print('  Avg. Time / solution', avg_evalTimePerCandidate, 'ms')
