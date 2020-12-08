'''
AMMM P2 Instance Generator v2.0
Instance Generator class.
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

import os, random
from AMMMGlobals import AMMMException


class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        nLocations = self.config.nLocations
        nCities = self.config.nCities
        nTypes = self.config.nTypes

        min_d_city = self.config.min_d_city
        max_d_city = self.config.max_d_city
        min_cap = self.config.min_cap
        max_cap = self.config.max_cap
        min_cost = self.config.min_cost
        max_cost = self.config.max_cost

        min_pos = 0
        max_pos = int((nLocations + nCities) / 2)

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            p = [0] * nCities
            for c in range(nCities):
                p[c] = random.randint(min_cap, max_cap)

            posCities = [''] * nCities
            for id, x in enumerate(posCities):
                newValue = self.create_locations(min_pos, max_pos, posCities)
                posCities[id] = newValue

            posLocations = [''] * nLocations
            for idx, x in enumerate(posLocations):
                newValue = self.create_locations(min_pos, max_pos, posLocations)
                posLocations[idx] = newValue

            d_city = [0] * nTypes
            cap = [0] * nTypes
            cost = [0] * nTypes
            for t in range(nTypes):
                d_city[t] = random.randint(min_d_city, max_d_city)
                cap[t] = random.randint(min_cap * 2, max_cap * 2)
                cost[t] = random.randint(min_cost, max_cost)

            d_center = random.uniform(min_pos, max_pos / 2)

            fInstance.write('nLocations = %d;\n' % nLocations)
            fInstance.write('nCities = %d;\n' % nCities)
            fInstance.write('nTypes = %d;\n' % nTypes)
            fInstance.write('\n')

            # translate vector of floats into vector of strings and concatenate that strings separating them by a single space character
            fInstance.write('p = [%s];\n' % (' '.join(map(str, p))))
            fInstance.write('posCities = [%s];\n' % (' '.join(map(str, posCities))))
            fInstance.write('posLocations = [%s];\n' % (' '.join(map(str, posLocations))))
            fInstance.write('\n')
            fInstance.write('d_city = [%s];\n' % (' '.join(map(str, d_city))))
            fInstance.write('cap = [%s];\n' % (' '.join(map(str, cap))))
            fInstance.write('cost = [%s];\n' % (' '.join(map(str, cost))))
            fInstance.write('\n')
            fInstance.write('d_center = %s;\n' % "{:.1f}".format(d_center))

            fInstance.close()

    def create_locations(self, min_pos, max_pos, posLocations):
        value1 = random.randint(min_pos, max_pos)
        value2 = random.randint(min_pos, max_pos)
        newValue = '[%d %d]' % (value1, value2)
        if newValue in posLocations:
            return self.create_locations(min_pos, max_pos, posLocations)
        else:
            return newValue
