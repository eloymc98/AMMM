"""
AMMM Lab Heuristics
Instance file validator v2.0
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


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['nLocations', 'nCities', 'nTypes', 'p', 'posCities', 'posLocations', 'd_city', 'cap', 'cost',
                          'd_center']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate nLocations
        nLocations = data.nLocations
        if not isinstance(nLocations, int) or (nLocations <= 0):
            raise AMMMException('nLocations(%s) has to be a positive integer value.' % str(nLocations))

        # Validate nCities
        nCities = data.nCities
        if not isinstance(nCities, int) or (nCities <= 0):
            raise AMMMException('nCities(%s) has to be a positive integer value.' % str(nCities))

        # Validate nTypes
        nTypes = data.nTypes
        if not isinstance(nTypes, int) or (nTypes <= 0):
            raise AMMMException('nTypes(%s) has to be a positive integer value.' % str(nTypes))

        # Validate p
        data.p = list(data.p)
        p = data.p
        if len(p) != nCities:
            raise AMMMException('Size of p(%d) does not match with value of nCities(%d).' % (len(p), nCities))

        for value in p:
            if not isinstance(value, (int, float)) or (value < 0):
                raise AMMMException(
                    'Invalid parameter value(%s) in p. Should be a float greater or equal than zero.' % str(value))

        # Validate posCities
        data.posCities = list(data.posCities)
        for i, v in enumerate(data.posCities):
            data.posCities[i] = list(data.posCities[i])
        posCities = data.posCities
        if len(posCities) != nCities:
            raise AMMMException('Size of posCities(%d) does not match with value of nCities(%d).' % (len(p), nCities))

        for value in posCities:
            for value2 in value:
                if not isinstance(value2, (int, float)) or (value2 < 0):
                    raise AMMMException(
                        'Invalid parameter value(%s) in posCities. Should be a float greater or equal than zero.' % str(
                            value2))

        # Validate posLocations
        data.posLocations = list(data.posLocations)
        for i, v in enumerate(data.posLocations):
            data.posLocations[i] = list(data.posLocations[i])
        posLocations = data.posLocations
        if len(posLocations) != nLocations:
            raise AMMMException(
                'Size of posLocations(%d) does not match with value of nLocations(%d).' % (len(p), nLocations))

        for value in posLocations:
            for value2 in value:
                if not isinstance(value2, (int, float)) or (value2 < 0):
                    raise AMMMException(
                        'Invalid parameter value(%s) in posLocations. Should be a float greater or equal than zero.' % str(
                            value))

        # Validate d_city
        data.d_city = list(data.d_city)
        d_city = data.d_city
        if len(d_city) != nTypes:
            raise AMMMException('Size of d_city(%d) does not match with value of nTypes(%d).' % (len(d_city), nTypes))

        for value in d_city:
            if not isinstance(value, (int, float)) or (value < 0):
                raise AMMMException(
                    'Invalid parameter value(%s) in d_city. Should be a float greater or equal than zero.' % str(value))

        # Validate cap
        data.cap = list(data.cap)
        cap = data.cap
        if len(cap) != nTypes:
            raise AMMMException('Size of cap(%d) does not match with value of nTypes(%d).' % (len(cap), nTypes))

        for value in cap:
            if not isinstance(value, (int, float)) or (value < 0):
                raise AMMMException(
                    'Invalid parameter value(%s) in cap. Should be a float greater or equal than zero.' % str(value))

        # Validate cost
        data.cost = list(data.cost)
        cost = data.cost
        if len(cost) != nTypes:
            raise AMMMException('Size of cost(%d) does not match with value of nTypes(%d).' % (len(cost), nTypes))

        for value in cost:
            if not isinstance(value, (int, float)) or (value < 0):
                raise AMMMException(
                    'Invalid parameter value(%s) in cost. Should be a float greater or equal than zero.' % str(value))

        # Validate d_center
        d_center = data.d_center
        if not isinstance(d_center, (int, float)) or (d_center < 0):
            raise AMMMException(
                'Invalid parameter value(%s) in d_center. Should be a float greater or equal than zero.' % str(
                    d_center))
