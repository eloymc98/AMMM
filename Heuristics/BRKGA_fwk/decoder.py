'''
AMMM Lab Heuristics
Abstract Decoder class
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

class _Decoder(object):
    def __init__(self, config, instance):
        self.config = config
        self.instance = instance

    def decode(self, generation):
        numDecoded = 0
        bestInGeneration = {'chr':None, 'solution':None, 'fitness':float('inf')}
        for individual in generation:
            numDecoded += 1
            if individual['fitness'] is None:
                solution, fitness = self.decodeIndividual(individual['chr'])
                individual['solution'] = solution
                individual['fitness'] = fitness
            if individual['fitness'] < bestInGeneration['fitness']:
                bestInGeneration = individual
        return bestInGeneration, numDecoded

    def getConfiguration(self):
        return self.config

    def decodeIndividual(self, chromosome):
        raise NotImplementedError