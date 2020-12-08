'''
AMMM P2 Instance Generator v2.0
Config attributes validator.
Copyright 2020 Luis Velasco

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

from AMMMGlobals import AMMMException


class ValidateConfig(object):
    # Validate config attributes read from a DAT file.

    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        paramList = ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                      'nLocations', 'nCities', 'nTypes',
                      'min_d_city', 'max_d_city', 'min_cap', 'max_cap', 'min_cost', 'max_cost']
        for paramName in paramList:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter(%s) has not been not specified in Configuration' % str(paramName))

        instancesDirectory = data.instancesDirectory
        if len(instancesDirectory) == 0: raise AMMMException('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if len(fileNamePrefix) == 0: raise AMMMException('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if len(fileNameExtension) == 0: raise AMMMException('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if not isinstance(numInstances, int) or (numInstances <= 0):
            raise AMMMException('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        nLocations = data.nLocations
        if not isinstance(nLocations, int) or (nLocations <= 0):
            raise AMMMException('nLocations(%s) has to be a positive integer value.' % str(nLocations))

        nCities = data.nCities
        if not isinstance(nCities, int) or (nCities <= 0):
            raise AMMMException('nCities(%s) has to be a positive integer value.' % str(nCities))

        nTypes = data.nTypes
        if not isinstance(nTypes, int) or (nTypes <= 0):
            raise AMMMException('nTypes(%s) has to be a positive integer value.' % str(nTypes))

        min_d_city = data.min_d_city
        if not isinstance(min_d_city, int) or (min_d_city <= 0):
            raise AMMMException('min_d_city(%s) has to be a positive integer value.' % str(min_d_city))

        max_d_city = data.max_d_city
        if not isinstance(max_d_city, int) or (max_d_city <= 0):
            raise AMMMException('max_d_city(%s) has to be a positive integer value.' % str(max_d_city))

        min_cap = data.min_cap
        if not isinstance(min_cap, (int, float)) or (min_cap <= 0):
            raise AMMMException('min_cap(%s) has to be a positive float value.' % str(min_cap))

        max_cap = data.max_cap
        if not isinstance(max_cap, (int, float)) or (max_cap <= 0):
            raise AMMMException('min_d_city(%s) has to be a positive float value.' % str(max_cap))

        min_cost = data.min_cost
        if not isinstance(min_cost, (int, float)) or (min_cost <= 0):
            raise AMMMException('min_d_city(%s) has to be a positive float value.' % str(min_cost))

        max_cost = data.max_cost
        if not isinstance(max_cost, (int, float)) or (max_cost <= 0):
            raise AMMMException('max_cost(%s) has to be a positive float value.' % str(max_cost))

        if max_cost < min_cost:
            raise AMMMException('max_cost(%s) has to be >= min_cost(%s).' % (str(max_cost), str(min_cost)))

        if max_cap < min_cap:
            raise AMMMException('max_cap(%s) has to be >= min_cap(%s).' % (str(max_cap), str(max_cap)))

        if max_d_city < min_d_city:
            raise AMMMException('max_d_city(%s) has to be >= min_d_city(%s).' % (str(max_d_city), str(min_d_city)))
