'''
AMMM Lab Heuristics
BRKGA solver
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
from Heuristics.solver import _Solver
from Heuristics.BRKGA_fwk.population import Population


class Solver_BRKGA(_Solver):

    def __init__(self, decoder, instance):
        self.decoder = decoder
        config = decoder.getConfiguration()
        self.population = Population(config)
        super().__init__(config, instance)

    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return self.elapsedEvalTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()

        incumbent = self.population.createDeterministicIndividual()
        initialSolution = kwargs.get('solution', None)
        if initialSolution is not None:
            incumbent['solution'] = initialSolution
            incumbent['fitness'] = initialSolution.getFitness()
            self.population.setIndividual(incumbent, 0)
        else:
            incumbent['solution'] = None
            incumbent['fitness'] = float('inf')
        self.writeLogLine(incumbent['fitness'], 0)

        generation = 0
        individualsDecoded = 0
        while True:
            generation += 1
            bestIndividual, numDecoded = self.decoder.decode(self.population.getGeneration())
            individualsDecoded += numDecoded
            if incumbent['fitness'] > bestIndividual['fitness']:
                incumbent = bestIndividual
                self.writeLogLine(incumbent['fitness'], generation)
            if self.stopCriteria(): break;
            elites, nonElites = self.population.classifyIndividuals()
            mutants = self.population.generateMutantIndividuals()
            crossover = self.population.doCrossover(elites, nonElites)
            self.population.setGeneration(elites + crossover + mutants)

        self.writeLogLine(incumbent['fitness'], generation)
        self.numSolutionsConstructed = individualsDecoded
        self.printPerformance()
        return incumbent['solution']


