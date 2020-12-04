'''
AMMM Lab Heuristics
BRKGA population class
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

import random
from AMMMGlobals import AMMMException


class Population(object):

    def __init__(self, config):
        self.config = config
        self.currentGeneration = [0] * config.numIndividuals
        for idx in range(config.numIndividuals):
            chromosome = [random.random() for i in range(config.numGenes)]
            self.currentGeneration[idx] = {'chr':chromosome, 'solution':{}, 'fitness':None}

    def createDeterministicIndividual(self):
        chromosome = [1] * self.config.numGenes
        return {'chr':chromosome, 'solution':None, 'fitness':None}

    def getGeneration(self):
        return self.currentGeneration

    def setGeneration(self, newGeneration):
        if newGeneration is None or len(newGeneration) != self.config.numIndividuals:
            raise AMMMException("ERROR: trying to set store a wrong generation vector")
        self.currentGeneration = newGeneration

    def setIndividual(self, individual, idx):
        if 0 > idx >= self.config.numIndividuals:
            raise AMMMException("ERROR: trying to set an individual in index: %s" % idx)
        self.currentGeneration[idx] = individual

    def classifyIndividuals(self):
        orderedGeneration = sorted(self.currentGeneration, key=lambda x: x['fitness'])
        elites=orderedGeneration[0:self.config.numElite]
        nonElites=orderedGeneration[self.config.numElite:len(self.currentGeneration)]
        return elites, nonElites

    def generateMutantIndividuals(self):
        mutants=[0] * self.config.numMutants
        for idx in range(self.config.numMutants):
            chromosome = [random.random() for i in range(self.config.numGenes)]
            mutants[idx] = {'chr':chromosome, 'solution':None, 'fitness':None}
        return mutants

    def doCrossover(self, elites, nonElites):
        crossover = [0] * self.config.numCrossover
        for idx in range(self.config.numCrossover):
            chrElite = random.choice(elites)['chr']
            chrNonElite = random.choice(nonElites)['chr']
            chrCross=[chrElite[gene] if random.random() <= self.config.inheritanceProb else chrNonElite[gene] for gene in range(self.config.numGenes)]
            crossover[idx] = {'chr':chrCross, 'solution':None,'fitness':None}
        return crossover
